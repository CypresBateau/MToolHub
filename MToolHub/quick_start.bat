@echo off
REM MToolHub 快速启动脚本 (Windows)
REM 用途：自动化完成数据导入、索引构建和服务启动

setlocal enabledelayedexpansion

echo ========================================
echo    MToolHub 快速启动脚本 (Windows)
echo ========================================
echo.

REM 检查 .env 文件
if not exist .env (
    echo [错误] 未找到 .env 文件
    echo 请创建 .env 文件并设置 CLAUDE_API_KEY
    echo.
    echo 示例：
    echo   echo CLAUDE_API_KEY=your_api_key_here ^> .env
    exit /b 1
)

echo [OK] 找到 .env 文件
echo.

REM 步骤 1: 启动基础服务
echo [步骤 1/5] 启动 Gateway 和工具服务...
docker compose up -d gateway tool-mdcalc tool-unit mavl

echo [等待] 服务启动中（30 秒）...
timeout /t 30 /nobreak >nul

REM 检查 Gateway 健康状态
echo [检查] Gateway 状态...
curl -s http://localhost:9000/tools >nul 2>&1
if errorlevel 1 (
    echo [错误] Gateway 未响应，请检查日志：
    echo    docker compose logs gateway
    exit /b 1
)
echo [OK] Gateway 运行正常
echo.

REM 步骤 2: 导入工具和模型
echo [步骤 2/5] 从 Gateway 导入工具和模型...
cd MToolHub\backend
python scripts\import_from_gateway.py

if not exist data\registry\tools.json (
    echo [错误] 工具导入失败
    exit /b 1
)
echo [OK] 工具和模型导入完成
echo.

REM 步骤 3: 导入技能
echo [步骤 3/5] 导入技能...
python scripts\import_skills.py

if not exist data\registry\skills.json (
    echo [错误] 技能导入失败
    exit /b 1
)
echo [OK] 技能导入完成
echo.

REM 步骤 4: 构建 FAISS 索引
echo [步骤 4/5] 构建 FAISS 索引...
python scripts\build_index.py

if not exist data\indexes\faiss.index (
    echo [错误] 索引构建失败
    exit /b 1
)
echo [OK] FAISS 索引构建完成
echo.

REM 返回项目根目录
cd ..\..

REM 步骤 5: 启动 MToolHub
echo [步骤 5/5] 启动 MToolHub 服务...
docker compose up -d mtoolhub

echo [等待] MToolHub 启动中（20 秒）...
timeout /t 20 /nobreak >nul

REM 验证部署
echo.
echo [验证] 检查部署状态...

REM 检查健康状态
curl -s http://localhost:8080/api/health | findstr "healthy" >nul 2>&1
if errorlevel 1 (
    echo [错误] MToolHub 健康检查失败
    echo 查看日志：
    echo    docker compose logs mtoolhub
    exit /b 1
)
echo [OK] MToolHub 健康检查通过

REM 检查资源数量
for /f "tokens=2 delims=:" %%a in ('curl -s http://localhost:8080/api/tools ^| findstr "count"') do (
    set COUNT=%%a
)
echo [OK] 已加载资源

echo.
echo ========================================
echo    MToolHub 启动完成！
echo ========================================
echo.
echo 服务地址：
echo    - MToolHub API: http://localhost:8080
echo    - API 文档: http://localhost:8080/docs
echo    - Gateway: http://localhost:9000
echo.
echo 快速测试：
echo    curl -X POST http://localhost:8080/api/chat ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"message\": \"帮我计算 Wells DVT 评分\"}"
echo.
echo 查看文档：
echo    type MToolHub\README.md
echo.
echo 查看日志：
echo    docker compose logs -f mtoolhub
echo.

endlocal
