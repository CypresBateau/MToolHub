# Med-Calc API 文档

> 机器可读版本：`API_DOC.json`

**调用方式：** `POST /tools/{tool-scale 或 tool-unit}/call`

```json
{"function_name": "...", "arguments": {"param": value}}
```

---

## 一、临床评分计算器（tool-scale，44 个）

| # | function_name | 工具名称 | 参数数量 |
|---|--------------|---------|----------|
| 1 | `calculate_ariscat_score` | ARISCAT Score for Postoperative Pulmonary Complications | 7 |
| 2 | `calculate_mme` | Morphine Milligram Equivalents (MME) Calculator | 3 |
| 3 | `calculate_centor_score` | Centor Score (Modified/McIsaac) for Strep Pharyngitis | 5 |
| 4 | `calculate_free_water_deficit` | Free Water Deficit in Hypernatremia | 4 |
| 5 | `calculate_wells_criteria` | Wells' Criteria for Pulmonary Embolism | 7 |
| 6 | `calculate_anion_gap` | Anion Gap | 3 |
| 7 | `calculate_phq9` | PHQ-9 (Patient Health Questionnaire-9) | 9 |
| 8 | `calculate_gad_7` | GAD-7 (General Anxiety Disorder-7) | 7 |
| 9 | `calculate_ciwa_ar` | CIWA-Ar for Alcohol Withdrawal | 9 |
| 10 | `calculate_revised_cardiac_risk_index` | Revised Cardiac Risk Index for Pre-Operative Risk | 6 |
| 11 | `calculate_heart_score` | HEART Score for Major Cardiac Events | 0 |
| 12 | `calculate_apache_ii_score` | APACHE II Score | 17 |
| 13 | `calculate_fib4` | Fibrosis-4 (FIB-4) Index for Liver Fibrosis | 4 |
| 14 | `calculate_bmi_bsa` | Body Mass Index (BMI) and Body Surface Area (BSA) | 2 |
| 15 | `corrected_calcium` | Calcium Correction for Hypoalbuminemia | 0 |
| 16 | `calculate_homa_ir` | HOMA-IR (Homeostatic Model Assessment for Insulin Resistance) | 2 |
| 17 | `curb_65_score` | CURB-65 Score for Pneumonia Severity | 5 |
| 18 | `calculate_psi_port_score` | PSI/PORT Score: Pneumonia Severity Index for CAP | 20 |
| 19 | `calculate_child_pugh_score` | Child-Pugh Score for Cirrhosis Mortality | 5 |
| 20 | `calculate_perc_rule` | PERC Rule for Pulmonary Embolism | 8 |
| 21 | `calculate_wells_criteria_dvt` | Wells' Criteria for DVT | 10 |
| 22 | `calculate_framingham_risk_score` | Framingham Risk Score for Hard Coronary Heart Disease | 7 |
| 23 | `calculate_ckd_epi_gfr` | CKD-EPI Equations for Glomerular Filtration Rate (GFR) | 3 |
| 24 | `calculate_caprini_score` | Caprini Score for Venous Thromboembolism (2005) | 34 |
| 25 | `calculate_stop_bang_score` | STOP-BANG Score for Obstructive Sleep Apnea | 8 |
| 26 | `calculate_gupta_perioperative_risk` | Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA) | 5 |
| 27 | `calculate_due_date` | Pregnancy Due Dates Calculator | 2 |
| 28 | `calculate_creatinine_clearance` | Creatinine Clearance (Cockcroft-Gault Equation) | 4 |
| 29 | `calculate_qtc` | Corrected QT Interval (QTc) | 3 |
| 30 | `sodium_correction_hyperglycemia` | Sodium Correction for Hyperglycemia | 2 |
| 31 | `calculate_glasgow_blatchford_score` | Glasgow-Blatchford Bleeding Score (GBS) | 9 |
| 32 | `calculate_fena` | Fractional Excretion of Sodium (FENa) | 4 |
| 33 | `calculate_glasgow_coma_scale` | Glasgow Coma Scale/Score (GCS) | 3 |
| 34 | `calculate_ibw_abw` | Ideal Body Weight and Adjusted Body Weight | 3 |
| 35 | `calculate_SOFA_score` | Sequential Organ Failure Assessment (SOFA) Score | 10 |
| 36 | `calculate_ldl` | LDL Calculated | 3 |
| 37 | `calculate_nihss` | NIH Stroke Scale/Score (NIHSS) | 15 |
| 38 | `calculate_maintenance_fluids` | Maintenance Fluids Calculations | 1 |
| 39 | `calculate_mean_arterial_pressure` | Mean Arterial Pressure (MAP) | 2 |
| 40 | `calculate_mdrd_gfr` | MDRD GFR Equation | 4 |
| 41 | `calculate_meld_na_unos_optn` | MELD Na (UNOS/OPTN) | 6 |
| 42 | `calculate_cha2ds2_vasc_score` | CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk | 7 |
| 43 | `calculate_has_bled_score` | HAS-BLED Score for Major Bleeding Risk | 9 |
| 44 | `calculate_serum_osmolality` | Serum Osmolality/Osmolarity | 3 |

---

### 1. `calculate_ariscat_score`

**工具名称：** ARISCAT Score for Postoperative Pulmonary Complications

**功能：** The ARISCAT score is a tool used to assess the risk of postoperative pulmonary complications (PPCs) in patients undergoing surgery.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | Patient's age in years |
| `spo2` | `int` | Preoperative oxygen saturation (SpO2) percentage |
| `respiratory_infection` | `int` | Indicates the presence of respiratory infection in the last month. 0 for 'No', 1 for 'Yes' |
| `anemia` | `int` | Indicates preoperative anemia (Hgb ≤10 g/dL). 0 for 'No', 1 for 'Yes' |
| `surgical_incision` | `int` | Type of surgical incision. 0 for 'Peripheral', 1 for 'Upper abdominal', 2 for 'Intrathoracic' |
| `surgery_duration` | `int` | Duration of the surgery in hours |
| `emergency` | `int` | Indicates if the procedure was an emergency. 0 for 'No', 1 for 'Yes' |

**返回值：** `int` — The ARISCAT score, which is a summation of points based on the provided parameters

---

### 2. `calculate_mme`

**工具名称：** Morphine Milligram Equivalents (MME) Calculator

**功能：** The Morphine Milligram Equivalents (MME) Calculator is used to convert various opioid dosages into a standardized morphine equivalent to help assess opioid use risk and ensure safe dosing.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `dosages` | `list of float` | List of dosages for each drug in the units appropriate for the drug |
| `doses_per_day` | `list of int` | List of doses per day for each corresponding drug |
| `drugs` | `list of int` | List of indexes representing drugs where each index corresponds to: |

**返回值：** `float` — Total MME/day calculated across all provided drugs

---

### 3. `calculate_centor_score`

**工具名称：** Centor Score (Modified/McIsaac) for Strep Pharyngitis

**功能：** The Centor Score, also known as the Modified Centor Score or McIsaac Score, is a clinical tool used to assess the likelihood of streptococcal pharyngitis in patients presenting with a sore throat.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | Age of the patient in years |
| `exudate_swelling` | `bool` | True if there is exudate or swelling on the tonsils, False otherwise |
| `tender_swollen_lymph_nodes` | `bool` | True if there are tender/swollen anterior cervical lymph nodes, False otherwise |
| `temperature` | `float` | Patient's temperature in degrees Celsius |
| `cough` | `bool` | True if cough is present, False otherwise |

**返回值：** `int` — The calculated Centor Score, which ranges from -1 to 4

---

### 4. `calculate_free_water_deficit`

**工具名称：** Free Water Deficit in Hypernatremia

**功能：** The Free Water Deficit (FWD) calculation is used in the management of hypernatremia to estimate the amount of water required to normalize a patient's serum sodium concentration.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `gender_age_group` | `int` | Index representing the patient's gender and age group |
| `weight_kg` | `float` | The weight of the patient in kilograms |
| `current_na` | `float` | The current serum sodium level of the patient (mmol/L) |
| `ideal_na` | `float` | The target or ideal serum sodium level for the patient (mmol/L) |

**返回值：** `float` — The calculated free water deficit in liters

---

### 5. `calculate_wells_criteria`

**工具名称：** Wells' Criteria for Pulmonary Embolism

**功能：** Wells' Criteria for Pulmonary Embolism is a clinical tool used to assess the probability of pulmonary embolism (PE) in patients presenting with symptoms suggestive of this condition.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `dvt_symptoms` | `bool` | True if there are clinical signs and symptoms of deep vein thrombosis (DVT), else False |
| `pe_diagnosis` | `bool` | True if pulmonary embolism is the #1 diagnosis or equally likely, else False |
| `heart_rate` | `bool` | True if heart rate is over 100, else False |
| `immobilization_surgery` | `bool` | True if patient has been immobilized for at least 3 days or had surgery in the past 4 weeks, else False |
| `previous_pe_dvt` | `bool` | True if there is a history of previously diagnosed PE or DVT, else False |
| `hemoptysis` | `bool` | True if the patient has hemoptysis, else False |
| `malignancy` | `bool` | True if the patient has malignancy with treatment within the last 6 months or is on palliative, else False |

**返回值：** `float` — The total score based on Wells' Criteria, which can be used to estimate the risk of pulmonary embolism

---

### 6. `calculate_anion_gap`

**工具名称：** Anion Gap

**功能：** The Anion Gap is a diagnostic tool used to help identify disturbances in acid-base balance in the body, typically by calculating the difference between primary measured cations and anions in serum.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `sodium` | `float` | Sodium level in mEq/L |
| `chloride` | `float` | Chloride level in mEq/L |
| `bicarbonate` | `float` | Bicarbonate level in mEq/L |

**返回值：** `float` — The calculated Anion Gap in mEq/L

---

### 7. `calculate_phq9`

**工具名称：** PHQ-9 (Patient Health Questionnaire-9)

**功能：** The PHQ-9 (Patient Health Questionnaire-9) is a widely used self-administered diagnostic tool for assessing the presence and severity of depression.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `interest_pleasure` | `int` | Index from 0 to 3 indicating frequency of little interest or pleasure in doing things |
| `feeling_down` | `int` | Index from 0 to 3 indicating frequency of feeling down, depressed, or hopeless |
| `sleep_issues` | `int` | Index from 0 to 3 indicating trouble with falling or staying asleep, or sleeping too much |
| `tired_energy` | `int` | Index from 0 to 3 indicating feeling tired or having little energy |
| `appetite_issues` | `int` | Index from 0 to 3 indicating issues with poor appetite or overeating |
| `self_feeling` | `int` | Index from 0 to 3 indicating feelings of being bad about oneself, or feeling like a failure |
| `concentration` | `int` | Index from 0 to 3 indicating trouble concentrating on things |
| `activity_level` | `int` | Index from 0 to 3 indicating altered activity levels, either moving too slowly or being too fidgety |
| `suicidal_thoughts` | `int` | Index from 0 to 3 indicating frequency of thoughts of self-harm or being better off dead |

**返回值：** `int` — The total PHQ-9 score, which is the sum of all the individual scores for the symptoms listed above

---

### 8. `calculate_gad_7`

**工具名称：** GAD-7 (General Anxiety Disorder-7)

**功能：** The GAD-7 (General Anxiety Disorder-7) is a self-administered questionnaire used to screen for and measure the severity of generalized anxiety disorder.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `nervous` | `int` | Score for feeling nervous, anxious, or on edge |
| `control_worrying` | `int` | Score for not being able to stop or control worrying |
| `worry_too_much` | `int` | Score for worrying too much about different things |
| `trouble_relaxing` | `int` | Score for having trouble relaxing |
| `restlessness` | `int` | Score for being so restless that it is hard to sit still |
| `irritability` | `int` | Score for becoming easily annoyed or irritable |
| `fear_of_awful_events` | `int` | Score for feeling afraid as if something awful might happen |

**返回值：** `int` — The total GAD-7 score, ranging from 0 to 21

---

### 9. `calculate_ciwa_ar`

**工具名称：** CIWA-Ar for Alcohol Withdrawal

**功能：** The Clinical Institute Withdrawal Assessment for Alcohol, Revised (CIWA-Ar) is a tool used to assess the severity of alcohol withdrawal symptoms and guide treatment decisions.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `nausea_vomiting` | `int` | Index for nausea and vomiting severity. Range: 0-7 |
| `tremor` | `int` | Index for tremor severity. Range: 0-7 |
| `paroxysmal_sweats` | `int` | Index for sweating severity. Range: 0-7 |
| `anxiety` | `int` | Index for anxiety level. Range: 0-7 |
| `agitation` | `int` | Index for agitation level. Range: 0-7 |
| `tactile_disturbances` | `int` | Index for tactile disturbances. Range: 0-7 |
| `visual_disturbances` | `int` | Index for visual disturbances. Range: 0-7 |
| `headache_fullness` | `int` | Index for headache or fullness in head. Range: 0-7 |
| `orientation_sensorium` | `int` | Index for orientation or clouding of sensorium. Range: 0-4 |

**返回值：** `int` — The total CIWA-Ar score, representing the severity of alcohol withdrawal

---

### 10. `calculate_revised_cardiac_risk_index`

**工具名称：** Revised Cardiac Risk Index for Pre-Operative Risk

**功能：** The Revised Cardiac Risk Index (RCRI) is a clinical tool used to estimate the risk of major cardiac complications, like heart attacks or cardiac arrest, in patients undergoing non-cardiac surgery.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `elevated_risk_surgery` | `bool` | True if the surgery is intraperitoneal, intrathoracic, or suprainguinal vascular |
| `history_of_ischemic_heart_disease` | `bool` | True if there is a history of myocardial infarction, positive exercise test, current chest pain considered due to myocardial ischemia, or use of nitrate therapy or ECG showing pathological Q waves |
| `history_of_congestive_heart_failure` | `bool` | True if there are signs such as pulmonary edema, bilateral rales or S3 gallop, paroxysmal nocturnal dyspnea, or chest X-ray showing pulmonary vascular redistribution |
| `history_of_cerebrovascular_disease` | `bool` | True if there is a history of transient ischemic attack or stroke |
| `preop_treatment_with_insulin` | `bool` | True if the patient is being treated with insulin pre-operatively |
| `preop_creatinine_above_threshold` | `bool` | True if pre-operative creatinine levels are greater than 2 mg/dL or 176.8 µmol/L |

**返回值：** `int` — The total Revised Cardiac Risk Index score, which is the sum of the individual risk factors present

---

### 11. `calculate_heart_score`

**工具名称：** HEART Score for Major Cardiac Events

**功能：** The HEART Score for Major Cardiac Events is a clinical tool used to assess the risk of major adverse cardiac events in patients presenting with chest pain.

**返回值：** `int` — The total HEART score, which can guide further management of chest pain patients

---

### 12. `calculate_apache_ii_score`

**工具名称：** APACHE II Score

**功能：** The APACHE II Score is a severity-of-disease classification system used in intensive care units(ICU) to predict severity and hospital mortality for critically ill patients.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | Age of the patient in years |
| `temperature` | `float` | Rectal temperature in degrees Celsius |
| `mean_arterial_pressure` | `int` | Mean arterial pressure in mm Hg |
| `heart_rate` | `int` | Heart rate in beats per minute |
| `respiratory_rate` | `int` | Respiratory rate in breaths per minute |
| `sodium` | `float` | Serum sodium in mmol/L |
| `potassium` | `float` | Serum potassium in mmol/L |
| `creatinine` | `float` | Serum creatinine in mg/100 mL |
| `hematocrit` | `float` | Hematocrit percentage |
| `white_blood_cell_count` | `float` | White blood cell count per cubic millimeter |
| `gcs` | `int` | Glasgow Coma Scale score, ranging from 3 (most impaired) to 15 (fully awake) |
| `ph` | `float` | Arterial pH |
| `history_of_severe_organ_insufficiency` | `int` | Indicates the patient's history status, with 0 for 'No', 1 for 'Yes, and elective postoperative patient', and 2 for 'Yes, and nonoperative or emergency postoperative patient' |
| `acute_renal_failure` | `int` | Indicates if the patient has acute renal failure, with 0 for 'No' and 1 for 'Yes' |
| `fio2` | `int` | Fraction of inspired oxygen, 0 for '<50%' and 1 for '≥50%' |
| `pao2` | `float, optional` | Partial pressure of arterial oxygen, required if FiO2 < 50% |
| `a_a_gradient` | `float, optional` | Alveolar-arterial gradient, required if FiO2 ≥ 50% |

**返回值：** `int` — The computed APACHE II score

---

### 13. `calculate_fib4`

**工具名称：** Fibrosis-4 (FIB-4) Index for Liver Fibrosis

**功能：** The Fibrosis-4 (FIB-4) Index is a clinical tool used to estimate the level of scarring, or fibrosis, in the liver, particularly helpful in assessing liver damage in patients with chronic liver diseases like hepatitis C and NAFLD.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int or float` | Age of the patient in years |
| `ast` | `float` | Aspartate aminotransferase level in U/L |
| `platelets` | `float` | Platelet count is measured in units of × 10⁹ per liter (× 10⁹ / L) |
| `alt` | `float` | Alanine aminotransferase level in U/L |

**返回值：** `float` — The FIB-4 Index score, which can be used to categorize liver fibrosis into mild,

---

### 14. `calculate_bmi_bsa`

**工具名称：** Body Mass Index (BMI) and Body Surface Area (BSA)

**功能：** The Body Mass Index (BMI) is a simple calculation used to assess whether an individual has a healthy body weight for a person of their height, widely used in general health assessments and public health studies.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `weight_kg` | `float` | Weight of the individual in kilograms |
| `height_cm` | `float` | Height of the individual in centimeters |

**返回值：** `dict` — Dictionary containing 'BMI' and 'BSA' with their respective values

---

### 15. `corrected_calcium`

**工具名称：** Calcium Correction for Hypoalbuminemia

**功能：** Calcium correction for hypoalbuminemia is used to accurately assess the level of bioavailable calcium in patients with low albumin levels, which can distort true calcium readings.

**返回值：** `float` — The corrected serum calcium level in mg/dL

---

### 16. `calculate_homa_ir`

**工具名称：** HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)

**功能：** The HOMA-IR (Homeostatic Model Assessment for Insulin Resistance) is a method used to assess insulin resistance, a key feature of conditions like type 2 diabetes and metabolic syndrome.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `fasting_insulin` | `float` | The fasting insulin level in uIU/mL |
| `fasting_glucose` | `float` | The fasting glucose level in mg/dL |

**返回值：** `float` — The estimated insulin resistance (HOMA-IR score)

---

### 17. `curb_65_score`

**工具名称：** CURB-65 Score for Pneumonia Severity

**功能：** The CURB-65 score is a clinical tool used to assess the severity of pneumonia and guide decisions regarding the need for hospitalization or intensive care.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `confusion` | `int` | Confusion status, where 0 = No and 1 = Yes |
| `bun` | `int` | Blood urea nitrogen status, where 0 = BUN ≤ 19 mg/dL (≤ 7 mmol/L urea) and 1 = BUN > 19 mg/dL (> 7 mmol/L urea) |
| `respiratory_rate` | `int` | Respiratory rate status, where 0 = < 30 breaths/min and 1 = ≥ 30 breaths/min |
| `blood_pressure` | `int` | Blood pressure status, where 0 = Systolic BP ≥ 90 mmHg and Diastolic BP > 60 mmHg, and 1 = Systolic BP < 90 mmHg or Diastolic BP ≤ 60 mmHg |
| `age` | `int` | Age status, where 0 = < 65 years and 1 = ≥ 65 years |

**返回值：** `int` — The CURB-65 score which ranges from 0 to 5, indicating the severity of pneumonia

---

### 18. `calculate_psi_port_score`

**工具名称：** PSI/PORT Score: Pneumonia Severity Index for CAP

**功能：** The Pneumonia Severity Index (PSI) or PORT Score is a clinical tool used to categorize the severity of community-acquired pneumonia (CAP) and assist in deciding the appropriate treatment setting.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | Patient's age in years |
| `sex` | `str` | Patient's sex, either 'Female' or 'Male' |
| `nursing_home_resident` | `bool` | True if the patient is a nursing home resident, False otherwise |
| `neoplastic_disease` | `bool` | True if the patient has a history of neoplastic disease, False otherwise |
| `liver_disease` | `bool` | True if the patient has a history of liver disease, False otherwise |
| `chf_history` | `bool` | True if the patient has a history of congestive heart failure, False otherwise |
| `cerebrovascular_disease` | `bool` | True if the patient has a history of cerebrovascular disease, False otherwise |
| `renal_disease` | `bool` | True if the patient has a history of renal disease, False otherwise |
| `altered_mental_status` | `bool` | True if the patient has altered mental status, False otherwise |
| `respiratory_rate` | `bool` | True if respiratory rate is ≥30 breaths/min, False otherwise |
| `systolic_bp` | `bool` | True if systolic blood pressure is <90 mmHg, False otherwise |
| `temperature` | `bool` | True if temperature is <35°C or >39.9°C, False otherwise |
| `pulse` | `bool` | True if pulse rate is ≥125 beats/min, False otherwise |
| `blood_ph` | `bool` | True if blood pH is <7.35, False otherwise |
| `bun` | `bool` | True if BUN is ≥30 mg/dL or ≥11 mmol/L, False otherwise |
| `sodium` | `bool` | True if sodium level is <130 mmol/L, False otherwise |
| `glucose` | `bool` | True if glucose level is ≥250 mg/dL or ≥14 mmol/L, False otherwise |
| `hematocrit` | `bool` | True if hematocrit is <30%, False otherwise |
| `oxygen_pressure` | `bool` | True if partial pressure of oxygen is <60 mmHg or <8 kPa, False otherwise |
| `pleural_effusion` | `bool` | True if there is pleural effusion on x-ray, False otherwise |

**返回值：** `int` — The total PSI/PORT Score indicating the severity of the pneumonia

---

### 19. `calculate_child_pugh_score`

**工具名称：** Child-Pugh Score for Cirrhosis Mortality

**功能：** The Child-Pugh Score is a clinical tool used to assess the prognosis of chronic liver disease, primarily cirrhosis.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `bilirubin` | `float` | Total bilirubin level in mg/dL |
| `albumin` | `float` | Albumin level in g/dL |
| `inr` | `float` | International Normalized Ratio |
| `ascites` | `str` | Describes the presence of ascites ('Absent', 'Slight', 'Moderate') |
| `encephalopathy` | `int` | Grade of hepatic encephalopathy (0 for none, 1-2 for Grade 1-2, 3-4 for Grade 3-4) |

**返回值：** `int` — The Child-Pugh Score, ranging from 5 (best) to 15 (worst)

---

### 20. `calculate_perc_rule`

**工具名称：** PERC Rule for Pulmonary Embolism

**功能：** The PERC (Pulmonary Embolism Rule-out Criteria) Rule is a clinical tool used to help physicians exclude pulmonary embolism (PE) in patients deemed low-risk without resorting to advanced imaging like CT scans.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age_over_50` | `bool` | Whether the patient is aged 50 or older. False for no, True for yes |
| `heart_rate_over_100` | `bool` | Whether the patient has a heart rate of 100 bpm or higher. False for no, True for yes |
| `oxygen_saturation_under_95` | `bool` | Whether the patient has an oxygen saturation less than 95%. False for no, True for yes |
| `unilateral_leg_swelling` | `bool` | Whether the patient has unilateral leg swelling. False for no, True for yes |
| `hemoptysis` | `bool` | Whether the patient has hemoptysis (coughing up blood). False for no, True for yes |
| `recent_surgery_or_trauma` | `bool` | Whether the patient had surgery or trauma within the last 4 weeks requiring general anesthesia. False for no, True for yes |
| `prior_pe_or_dvt` | `bool` | Whether the patient has a history of Pulmonary Embolism (PE) or Deep Vein Thrombosis (DVT). False for no, True for yes |
| `hormone_use` | `bool` | Whether the patient is using hormones such as oral contraceptives, hormone replacement therapy, or estrogenic hormones in male or female patients. False for no, True for yes |

**返回值：** `str` — 评分结果文本

---

### 21. `calculate_wells_criteria_dvt`

**工具名称：** Wells' Criteria for DVT

**功能：** Wells' Criteria for Deep Vein Thrombosis (DVT) is a clinical tool used to assess the probability of DVT in patients presenting with symptoms suggestive of this condition.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `active_cancer` | `bool` | True if the patient has active cancer (treatment within last 6 months) |
| `bedridden_recently` | `bool` | True if the patient was bedridden for more than 3 days recently or had major surgery within the last 12 weeks |
| `calf_swelling` | `bool` | True if the patient's calf swelling exceeds 3 cm compared to the other leg |
| `collateral_veins` | `bool` | True if collateral non-varicose superficial veins are present |
| `entire_leg_swollen` | `bool` | True if the entire leg is swollen |
| `localized_tenderness` | `bool` | True if there is localized tenderness along the deep venous system |
| `pitting_edema` | `bool` | True if there is pitting edema confined to the symptomatic leg |
| `recent_immobilization` | `bool` | True if the patient had paralysis, paresis, or recent plaster immobilization of the lower extremities |
| `previous_dvt` | `bool` | True if the patient has a history of documented DVT |
| `alternative_diagnosis` | `bool` | True if an alternative diagnosis is as likely or more likely than DVT |

**返回值：** `int` — Wells' score for DVT, where higher values indicate a higher probability of DVT

---

### 22. `calculate_framingham_risk_score`

**工具名称：** Framingham Risk Score for Hard Coronary Heart Disease

**功能：** The Framingham Risk Score for Hard Coronary Heart Disease is a tool used by healthcare professionals to estimate a patient's 10-year risk of developing severe heart disease.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | The age of the patient in years. Valid range: 30-79 |
| `sex` | `int` | The sex of the patient. 0 for female, 1 for male |
| `smoker_status` | `int` | Smoking status of the patient. 0 for non-smoker, 1 for smoker |
| `total_cholesterol` | `float` | Total cholesterol level in mg/dL |
| `hdl_cholesterol` | `float` | HDL cholesterol level in mg/dL |
| `systolic_bp` | `float` | Systolic blood pressure in mm Hg |
| `bp_medication` | `int` | Indicates if the blood pressure is being treated with medications. 0 for no, 1 for yes |

**返回值：** `float` — The risk percentage of developing hard coronary heart disease

---

### 23. `calculate_ckd_epi_gfr`

**工具名称：** CKD-EPI Equations for Glomerular Filtration Rate (GFR)

**功能：** The CKD-EPI (Chronic Kidney Disease Epidemiology Collaboration) equations are used to estimate the glomerular filtration rate (GFR), which is crucial for assessing kidney function.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `serum_creatinine` | `float` | The serum creatinine level of the patient in mg/dL |
| `age` | `int` | The age of the patient in years |
| `gender` | `int` | The gender of the patient. Use 0 for male and 1 for female |

**返回值：** `float` — The estimated GFR in ml/min/1.73m^2

---

### 24. `calculate_caprini_score`

**工具名称：** Caprini Score for Venous Thromboembolism (2005)

**功能：** The Caprini Score for Venous Thromboembolism (2005) is a risk assessment tool used to evaluate the likelihood of developing venous thromboembolism (VTE) in hospital patients.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | Patient's age in years |
| `sex` | `int` | Patient's sex (0 for male, 1 for female) |
| `surgery_type` | `int` | Type of surgery classified by duration and invasiveness (0 for none, 1 for minor, 2 for major, 5 for elective major lower extremity arthroplasty) |
| `recent_event` | `int` | Recent surgeries or events (0 for none, 1 for minor, 2 for major or laparoscopic over 45 min) |
| `major_surgery` | `int` | Whether the patient had major surgery (0 for no, 1 for yes) |
| `chf` | `int` | Congestive heart failure present (0 for no, 1 for yes) |
| `sepsis` | `int` | Sepsis present (0 for no, 1 for yes) |
| `pneumonia` | `int` | Pneumonia present (0 for no, 1 for yes) |
| `plaster_cast` | `int` | Presence of an immobilizing plaster cast (0 for no, 2 for yes) |
| `fracture` | `int` | Presence of hip, pelvis, or leg fracture (0 for no, 5 for yes) |
| `stroke` | `int` | History of stroke (0 for no, 5 for yes) |
| `multiple_trauma` | `int` | Presence of multiple traumas (0 for no, 5 for yes) |
| `spinal_injury` | `int` | Acute spinal cord injury causing paralysis (0 for no, 5 for yes) |
| `varicose_veins` | `int` | Presence of varicose veins (0 for no, 1 for yes) |
| `swollen_legs` | `int` | Currently swollen legs (0 for no, 1 for yes) |
| `central_venous_access` | `int` | Current central venous access (0 for no, 2 for yes) |
| `history_dvt_pe` | `int` | History of deep vein thrombosis or pulmonary embolism (0 for no, 3 for yes) |
| `family_thrombosis` | `int` | Family history of thrombosis (0 for no, 3 for yes) |
| `factor_v_leiden` | `int` | Positive Factor V Leiden mutation (0 for no, 3 for yes) |
| `prothrombin_20210A` | `int` | Positive prothrombin 20210A mutation (0 for no, 3 for yes) |
| `homocysteine` | `int` | Elevated serum homocysteine levels (0 for no, 3 for yes) |
| `lupus_anticoagulant` | `int` | Positive lupus anticoagulant (0 for no, 3 for yes) |
| `anticardiolipin_antibody` | `int` | Elevated anticardiolipin antibody levels (0 for no, 3 for yes) |
| `heparin_thrombocytopenia` | `int` | Heparin-induced thrombocytopenia (0 for no, 3 for yes) |
| `thrombophilia` | `int` | Other congenital or acquired thrombophilia (0 for no, 3 for yes) |
| `mobility` | `int` | Mobility status (0 for normal, out of bed, 1 for medical patient currently on bed rest, 2 for patient confined to bed >72 hours) |
| `ibd` | `int` | History of inflammatory bowel disease (0 for no, 1 for yes) |
| `bmi_over_25` | `int` | BMI over 25 (0 for no, 1 for yes) |
| `acute_mi` | `int` | Acute myocardial infarction (0 for no, 1 for yes) |
| `copd` | `int` | Chronic obstructive pulmonary disease (0 for no, 1 for yes) |
| `malignancy` | `int` | Presence or history of malignancy (0 for no, 2 for yes) |
| `other_risk_factors` | `int` | Other unspecified risk factors (0 for no, 1 for yes) |
| `contraceptives_hormones` | `int` | Use of oral contraceptives or hormone replacement therapy (0 for no, 1 for yes) |
| `reproductive_history` | `int` | History of unexplained stillborn, ≥3 spontaneous abortions, or premature birth with toxemia or growth-restricted infant (0 for no, 1 for yes) |

**返回值：** `int` — The calculated Caprini score

---

### 25. `calculate_stop_bang_score`

**工具名称：** STOP-BANG Score for Obstructive Sleep Apnea

**功能：** The STOP-BANG Score is a clinical tool used to screen individuals for obstructive sleep apnea (OSA).

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `snore_loudly` | `bool` | True if the patient snores loudly (louder than talking or loud enough to be heard through closed doors), False otherwise |
| `feel_tired_daytime` | `bool` | True if the patient often feels tired, fatigued, or sleepy during the daytime, False otherwise |
| `observed_apnea` | `bool` | True if anyone has observed the patient stop breathing during sleep, False otherwise |
| `high_blood_pressure` | `bool` | True if the patient has or is being treated for high blood pressure, False otherwise |
| `bmi` | `float` | Body Mass Index of the patient |
| `age` | `int` | Age of the patient in years |
| `neck_circumference` | `float` | Neck circumference of the patient in centimeters |
| `gender` | `str` | Gender of the patient. Expected values: 'Female' or 'Male' |

**返回值：** `int` — The total STOP-BANG score, ranging from 0 to 8

---

### 26. `calculate_gupta_perioperative_risk`

**工具名称：** Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA)

**功能：** The Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA) score is a clinical tool used to estimate the risk of myocardial infarction or cardiac arrest in patients undergoing surgery.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | The age of the patient in years |
| `functional_status` | `int` | Functional status of the patient |
| `asa_class` | `int` | ASA class of the patient |
| `creatinine` | `int` | Creatinine level status |
| `procedure_type` | `int` | Type of procedure being performed |

**返回值：** `float` — The estimated cardiac risk percentage

---

### 27. `calculate_due_date`

**工具名称：** Pregnancy Due Dates Calculator

**功能：** A Pregnancy Due Date Calculator is used to estimate the expected date of birth, commonly known as the due date, based on the first day of the last menstrual period or conception date.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `cycle_length` | `int` | The length of the menstrual cycle in days. Standard cycle is 28 days |
| `last_menstrual_period` | `str` | The first day of the last menstrual period in 'YYYY/MM/DD' format |

**返回值：** `str` — The estimated due date in the format 'Day, Month DD, YYYY'

---

### 28. `calculate_creatinine_clearance`

**工具名称：** Creatinine Clearance (Cockcroft-Gault Equation)

**功能：** Creatinine clearance, estimated using the Cockcroft-Gault equation, helps assess kidney function by estimating the rate at which the kidneys remove creatinine from the blood.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | The age of the patient in years. Should be a positive integer |
| `weight` | `float` | The weight of the patient in kilograms. Should be a positive decimal |
| `creatinine` | `float` | The serum creatinine level in mg/dL. Should be a positive decimal |
| `sex` | `str` | The sex of the patient. Acceptable values are 'male' or 'female' |

**返回值：** `float` — The estimated creatinine clearance in mL/min

---

### 29. `calculate_qtc`

**工具名称：** Corrected QT Interval (QTc)

**功能：** The Corrected QT Interval (QTc) is a measure used to assess the heart's electrical recovery period, adjusted for heart rate variations.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `qt_interval` | `float` | The measured QT interval in milliseconds |
| `heart_rate` | `float` | The patient's heart rate in beats per minute |
| `formula` | `str` | The formula to use for correction. Options are 'Bazett', 'Fridericia', |

**返回值：** `float` — The corrected QT interval (QTc) in milliseconds

---

### 30. `sodium_correction_hyperglycemia`

**工具名称：** Sodium Correction for Hyperglycemia

**功能：** Sodium correction for hyperglycemia is used to adjust the measured sodium level in the blood, which can be artificially lowered by high blood glucose levels.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `measured_sodium` | `float` | The measured sodium level in mEq/L |
| `serum_glucose` | `float` | The serum glucose level in mg/dL |

**返回值：** `float` — The corrected sodium level in mEq/L

---

### 31. `calculate_glasgow_blatchford_score`

**工具名称：** Glasgow-Blatchford Bleeding Score (GBS)

**功能：** The Glasgow-Blatchford Bleeding Score (GBS) is a clinical tool used to assess the severity of bleeding and the need for medical intervention in patients presenting with acute upper gastrointestinal bleeding.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `hemoglobin` | `float` | Patient's hemoglobin level in g/dL |
| `bun` | `float` | Blood Urea Nitrogen (BUN) level in mg/dL |
| `systolic_bp` | `int` | Initial systolic blood pressure in mm Hg |
| `sex` | `int` | Patient's sex, 0 for female, 1 for male |
| `heart_rate` | `int` | Indicates if heart rate is ≥100 per minute, 0 for no, 1 for yes |
| `melena` | `int` | Indicates if melena is present, 0 for no, 1 for yes |
| `syncope` | `int` | Indicates if there has been a recent syncope, 0 for no, 2 for yes |
| `hepatic_disease` | `int` | Indicates history of hepatic disease, 0 for no, 2 for yes |
| `cardiac_failure` | `int` | Indicates if cardiac failure is present, 0 for no, 2 for yes |

**返回值：** `int` — Glasgow-Blatchford Score, ranging from 0 to 23

---

### 32. `calculate_fena`

**工具名称：** Fractional Excretion of Sodium (FENa)

**功能：** The Fractional Excretion of Sodium (FENa) is a diagnostic tool used primarily to differentiate between pre-renal and intrinsic renal causes of acute kidney injury (AKI).

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `serum_creatinine` | `float` | Serum creatinine concentration (mg/dL) |
| `urine_sodium` | `float` | Urine sodium concentration (mmol/L) |
| `serum_sodium` | `float` | Serum sodium concentration (mmol/L) |
| `urine_creatinine` | `float` | Urine creatinine concentration (mg/dL) |

**返回值：** `float` — The Fractional Excretion of Sodium (FENa) in percentage

---

### 33. `calculate_glasgow_coma_scale`

**工具名称：** Glasgow Coma Scale/Score (GCS)

**功能：** The Glasgow Coma Scale (GCS) is a clinical tool used to assess a person's level of consciousness after a head injury.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `eye_response` | `int or str` | Score or 'NT' (not testable) for eye response |
| `verbal_response` | `int or str` | Score or 'NT' (not testable) for verbal response |
| `motor_response` | `int or str` | Score or 'NT' (not testable) for motor response |

**返回值：** `int or None` — Total GCS score if all components are testable, otherwise None

---

### 34. `calculate_ibw_abw`

**工具名称：** Ideal Body Weight and Adjusted Body Weight

**功能：** Ideal Body Weight (IBW) is used primarily to calculate drug dosages and medical needs where a standard weight is beneficial for clinical calculations.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `height_in_inches` | `int` | The height of the individual in inches |
| `actual_body_weight` | `float` | The actual body weight of the individual in kilograms |
| `gender` | `str` | The gender of the individual ("male" or "female") |

**返回值：** `list` — A list containing the IBW and ABW in kilograms. If the individual is not obese, ABW is set equal to IBW

---

### 35. `calculate_SOFA_score`

**工具名称：** Sequential Organ Failure Assessment (SOFA) Score

**功能：** The Sequential Organ Failure Assessment (SOFA) Score is a medical tool used to assess the extent of organ function or rate of failure in critically ill patients.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `pao2_fio2_ratio` | `float` | The ratio of arterial oxygen partial pressure to fractional inspired oxygen (mmHg) |
| `platelets` | `float` | Platelet count in ×103/µL |
| `glasgow_coma_scale` | `int` | Score on the Glasgow Coma Scale |
| `bilirubin` | `float` | Serum bilirubin in mg/dL |
| `map_pressure` | `float` | Mean arterial pressure in mmHg |
| `vasoactive_agents` | `int` | Index indicating the vasoactive agents being used. Corresponds to 0 for no agents, 1 for low dose dopamine or any dose dobutamine, 2 for higher dose dopamine or low dose epinephrine/norepinephrine, 3 for very high dose of these agents |
| `creatinine` | `float` | Serum creatinine in mg/dL |
| `urine_output` | `float` | Urine output in mL/day |
| `o2_delivery_type` | `int` | Index of the type of oxygen delivery method used. Types are as follows: 0 = nasal cannula, 1 = simple face mask, 2 = non-rebreather mask, 3 = high-flow nasal cannula |
| `o2_flow_rate` | `float` | Flow rate of oxygen delivery in L/min |

**返回值：** `int` — Total SOFA score which is the sum of individual scores across the specified parameters."

---

### 36. `calculate_ldl`

**工具名称：** LDL Calculated

**功能：** LDL Calculated, or LDL-C, is an estimation of the low-density lipoprotein cholesterol in the blood, often used to assess cardiovascular risk.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `total_cholesterol` | `float` | Total cholesterol level in mg/dL |
| `hdl` | `float` | High-Density Lipoprotein (HDL) cholesterol level in mg/dL |
| `triglycerides` | `float` | Triglyceride level in mg/dL, measured while fasting |

**返回值：** `float` — Estimated LDL cholesterol level in mg/dL

---

### 37. `calculate_nihss`

**工具名称：** NIH Stroke Scale/Score (NIHSS)

**功能：** The NIH Stroke Scale/Score (NIHSS) is a tool used by healthcare professionals to objectively quantify the impairment caused by a stroke.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `loc_alertness` | `int` | Level of consciousness - Alert (0), Arouses to minor stimulation (1), Requires repeated stimulation (2), Movements to pain (2), Postures or unresponsive (3) |
| `loc_questions` | `int` | Ask month and age - Both right (0), One right (1), None right (2), Dysarthric/intubated/trauma/language barrier (1), Aphasic (2) |
| `loc_commands` | `int` | 'Blink eyes' & 'squeeze hands' - Performs both (0), Performs one (1), Performs none (2) |
| `horizontal_gaze` | `int` | Horizontal extraocular movements - Normal (0), Partial palsy (1), Forced palsy (2) |
| `visual_fields` | `int` | Visual fields - No loss (0), Partial hemianopia (1), Complete hemianopia (2), Bilateral blindness (3), Bilateral hemianopia (3) |
| `facial_palsy` | `int` | Facial palsy - Normal (0), Minor (1), Partial (2), Unilateral complete (3), Bilateral complete (3) |
| `left_arm_motor_drift` | `int` | Left arm motor drift - No drift (0), Drift but doesn't hit bed (1), Drift, hits bed (2), Some effort against gravity (2), No effort against gravity (3), No movement (4), Amputation/joint fusion (0) |
| `right_arm_motor_drift` | `int` | Right arm motor drift - No drift (0), Drift but doesn't hit bed (1), Drift, hits bed (2), Some effort against gravity (2), No effort against gravity (3), No movement (4), Amputation/joint fusion (0) |
| `left_leg_motor_drift` | `int` | Left leg motor drift - No drift (0), Drift but doesn't hit bed (1), Drift, hits bed (2), Some effort against gravity (2), No effort against gravity (3), No movement (4), Amputation/joint fusion (0) |
| `right_leg_motor_drift` | `int` | Right leg motor drift - No drift (0), Drift but doesn't hit bed (1), Drift, hits bed (2), Some effort against gravity (2), No effort against gravity (3), No movement (4), Amputation/joint fusion (0) |
| `limb_ataxia` | `int` | Limb ataxia - No ataxia (0), Ataxia in 1 limb (1), Ataxia in 2 limbs (2), Does not understand (0), Paralyzed (0), Amputation/joint fusion (0) |
| `sensation` | `int` | Sensation - Normal (0), Mild-moderate loss (1), Mild-moderate loss (1), Complete loss (2), No response/quadriplegic (2), Coma/unresponsive (2) |
| `language_aphasia` | `int` | Language/aphasia - Normal (0), Mild-moderate aphasia (1), Severe aphasia (2), Mute/global aphasia (3), Coma/unresponsive (3) |
| `dysarthria` | `int` | Dysarthria - Normal (0), Mild-moderate (1), Severe (2), Mute/anarthric (2), Intubated/unable to test (0) |
| `extinction_inattention` | `int` | Extinction/inattention - No abnormality (0), Inattention (1), Extinction to bilateral stimulation (1), Profound hemi-inattention (2), Extinction to >1 modality (2) |

**返回值：** `int` — Total NIHSS score, summing all input values

---

### 38. `calculate_maintenance_fluids`

**工具名称：** Maintenance Fluids Calculations

**功能：** Maintenance fluids calculations are used in medical settings to determine the appropriate volume and composition of fluids required to keep a patient hydrated and maintain normal physiological functions, particularly when they cannot consume fluids orally.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `weight` | `float` | The weight of the patient in kilograms |

**返回值：** `float` — The calculated IV fluid rate in mL per hour

---

### 39. `calculate_mean_arterial_pressure`

**工具名称：** Mean Arterial Pressure (MAP)

**功能：** Mean Arterial Pressure (MAP) is a critical measurement used to assess the average blood pressure in a person's arteries during one cardiac cycle.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `systolic_bp` | `float` | Systolic blood pressure in mmHg |
| `diastolic_bp` | `float` | Diastolic blood pressure in mmHg |

**返回值：** `float` — The calculated mean arterial pressure in mmHg

---

### 40. `calculate_mdrd_gfr`

**工具名称：** MDRD GFR Equation

**功能：** The MDRD (Modification of Diet in Renal Disease) GFR Equation is used to estimate glomerular filtration rate (GFR), reflecting kidney function.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `serum_cr` | `float` | Serum creatinine (Cr) level in mg/dL. Should be a positive float |
| `age` | `int` | Age of the patient in years. Should be a non-negative integer |
| `race_index` | `int` | Index representing the patient's race. 0 for non-black, 1 for black |
| `gender_index` | `int` | Index representing the patient's gender. 0 for male, 1 for female |

**返回值：** `float` — Estimated GFR in ml/min/1.73m2

---

### 41. `calculate_meld_na_unos_optn`

**工具名称：** MELD Na (UNOS/OPTN)

**功能：** The MELD Na (Model for End-Stage Liver Disease Sodium) score, used by the United Network for Organ Sharing (UNOS) and the Organ Procurement and Transplantation Network (OPTN), is a critical tool in prioritizing liver transplant candidates.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `creatinine` | `float` | Serum creatinine in mg/dL. Minimum value used is 1.0. If patient's creatinine >4.0 or they received ≥2 dialysis treatments in the last 7 days or 24 hours of CVVHD, use 4.0 |
| `bilirubin` | `float` | Serum bilirubin in mg/dL. Minimum value used is 1.0 |
| `inr` | `float` | International Normalized Ratio (INR), unitless. Minimum value used is 1.0 |
| `sodium` | `float` | Serum sodium in mEq/L. Adjusted to be within the range of 125 to 137 mEq/L |
| `dialysis_treatments` | `int` | Number of dialysis treatments in the last 7 days. Default is 0 |
| `cvvhd_hours` | `int` | Hours of continuous veno-venous hemodialysis (CVVHD) within the last 7 days. Default is 0 |

**返回值：** `str` — 评分结果文本

---

### 42. `calculate_cha2ds2_vasc_score`

**工具名称：** CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk

**功能：** The CHA2DS2-VASc Score is a clinical tool used to estimate the risk of stroke in patients with atrial fibrillation.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `age` | `int` | Age of the patient |
| `sex` | `str` | Biological sex of the patient, 'male' or 'female' |
| `history_of_congestive_heart_failure` | `bool` | True if the patient has a history of congestive heart failure, otherwise False |
| `history_of_hypertension` | `bool` | True if the patient has a history of hypertension, otherwise False |
| `history_of_stroke_tia_thromboembolism` | `bool` | True if the patient has a history of stroke, transient ischemic attack (TIA), or thromboembolism, otherwise False |
| `history_of_vascular_disease` | `bool` | True if the patient has a history of vascular disease (prior myocardial infarction, peripheral artery disease, or aortic plaque), otherwise False |
| `history_of_diabetes` | `bool` | True if the patient has a history of diabetes mellitus, otherwise False |

**返回值：** `int` — The total CHA2DS2-VASc score which is a sum of the points for each risk factor

---

### 43. `calculate_has_bled_score`

**工具名称：** HAS-BLED Score for Major Bleeding Risk

**功能：** The HAS-BLED score is a clinical tool used to assess the risk of major bleeding in patients with atrial fibrillation who are on anticoagulation therapy.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `hypertension` | `bool` | True if the patient has hypertension, False otherwise |
| `renal_disease` | `bool` | True if the patient has renal disease (dialysis, transplant, or Cr >2.26 mg/dL), False otherwise |
| `liver_disease` | `bool` | True if the patient has liver disease (cirrhosis or bilirubin >2x normal with AST/ALT/AP >3x normal), False otherwise |
| `stroke_history` | `bool` | True if the patient has a history of stroke, False otherwise |
| `major_bleeding_history` | `bool` | True if the patient has had prior major bleeding or predisposition to bleeding, False otherwise |
| `labile_inr` | `bool` | True if the patient has labile INR (unstable/high INRs, time in therapeutic range <60%), False otherwise |
| `elderly` | `bool` | True if the patient is elderly (age >65), False otherwise |
| `medication_risk` | `bool` | True if the patient uses medication that predisposes to bleeding (aspirin, clopidogrel, NSAIDs), False otherwise |
| `alcohol_usage` | `bool` | True if the patient consumes alcohol significantly (≥8 drinks/week), False otherwise |

**返回值：** `int` — The total HAS-BLED score, which is a sum of all applicable risk factors

---

### 44. `calculate_serum_osmolality`

**工具名称：** Serum Osmolality/Osmolarity

**功能：** Serum osmolality or osmolarity measures the concentration of solutes in the blood, providing insights into the body's water balance and solute concentration.

**输入参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `serum_na` | `float` | Serum sodium concentration in mmol/L. Typical reference range is 135-145 mmol/L |
| `serum_glucose` | `float` | Serum glucose concentration in mg/dL. Typical reference range is 70-100 mg/dL |
| `serum_bun` | `float` | Blood urea nitrogen concentration in mg/dL. Typical reference range is 7-20 mg/dL |

**返回值：** `float` — Calculated serum osmolality in mOsm/kg

---

## 二、医学单位换算工具（tool-unit，237 个）

**输入参数（所有换算工具统一）：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `input_value` | `float` | 输入数值 |
| `input_unit` | `int` | 输入单位在 `units_list` 中的索引（0-based） |
| `target_unit` | `int` | 目标单位在 `units_list` 中的索引（0-based） |

**返回值（所有换算工具统一）：** `str` — 如 `"4.5 mmol/L = 4.5 mEq/L"`

| # | function_name | 检测物（中英文） | units_list |
|---|--------------|-----------------|------------|
| 1 | `convert_potassium_k_unit` | Potassium (K), 钾 (K) | mmol/L, mEq/L |
| 2 | `convert_prealbumin_unit` | Prealbumin, 前白蛋白 | µmol/L, g/L, g/dL, g/100mL, g%, mg/mL |
| 3 | `convert_pregnancy_associated_plasma_protein_A_unit` | Pregnancy-associated plasma protein A, 妊娠相关血浆蛋白 A | mIU/L, µIU/mL, IU/L, mIU/mL |
| 4 | `convert_procalcitonin_unit` | Procalcitonin, 降钙素原 | µg/L, ng/L, ng/dL, ng/100mL, ng%, ng/mL |
| 5 | `convert_progesterone_unit` | Progesterone, 黄体酮 | nmol/L, pmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 6 | `convert_gastrin_releasing_peptide_precursor_unit` | Gastrin-releasing peptide precursor, 胃泌素释放肽前体 | pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 7 | `convert_prolactin_unit` | Prolactin, 催乳素 | μg/L, μIU/mL, mIU/L, ng/mL, ng/dL, ng/100mL, ng% |
| 8 | `convert_proline_unit` | Proline, 脯氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 9 | `convert_prostate_specific_antigen_psa_unit` | Prostate-Specific Antigen (PSA), 前列腺特异性抗原 | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 10 | `convert_free_prostate_specific_antigen_unit` | Free Prostate-Specific Antigen, 游离前列腺特异性抗原 | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 11 | `convert_prothrombin_time_unit` | Prothrombin Time, 凝血酶原时间 | s, sec |
| 12 | `convert_prothrombin_time_quick_test_unit` | Prothrombin Time (Quick's Test), 凝血酶原时间(Quick检测法) | Ratio, Fraction, % |
| 13 | `convert_pyrrolysine_unit` | Pyrrolysine, 吡咯赖氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 14 | `convert_red_blood_cell_distribution_width_coefficient_of_variation_unit` | Red Blood Cell Distribution Width Coefficient of Variation, 红细胞分布宽度变异系数 | Proportion of 1.0, % |
| 15 | `convert_red_blood_cell_distribution_width_standard_deviation_unit` | Red Blood Cell Distribution Width Standard Deviation, 红细胞分布宽度标准差 | fL, µm^3 |
| 16 | `convert_red_blood_cell_unit` | Red Blood Cell, 红细胞 | 10^9/L, T/L, Tpt/L, cells/L, 106/µL (1000000/µL), 106/mm3 (1000000/mm3), M/µL, M/mm3, cells/µL, cells/mm^3 |
| 17 | `convert_renin_unit` | Renin, 肾素 | pmol/L, pg/mL, ng/dL, ng/100mL, ng% |
| 18 | `convert_retinol_unit` | Retinol, 视黄醇 | µmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL |
| 19 | `convert_rheumatoid_factor_unit` | Rheumatoid Factor, 类风湿因子 | U/mL, kU/L, IU/mL, kIU/L |
| 20 | `convert_Riboflavin_unit` | Riboflavin, 核黄素 | nmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL |
| 21 | `convert_s100_protein_unit` | S100 Protein, S100蛋白 | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 22 | `convert_salicylates_unit` | Salicylates, 水杨酸盐 | mmol/L, mg/dL, mg/100mL, mg%, mg/L, ng/mL |
| 23 | `convert_Selenocysteine_unit` | Selenocysteine, 硒代半胱氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 24 | `convert_serine_unit` | Serine, 丝氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, ng/mL |
| 25 | `convert_serotonin_unit` | Serotonin, 血清素 | µmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 26 | `convert_sex_hormone_binding_globulin_unit` | Sex Hormone Binding Globulin, 性激素结合球蛋白 | nmol/L, µg/mL, µg/dL, µg/100mL, µg%, µg/L, mg/L |
| 27 | `convert_soluble_fms_like_tyrosine_kinase_1_unit` | Soluble Fms-like tyrosine kinase 1, 可溶性Fms样酪氨酸激酶1 | pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 28 | `convert_sodium_unit` | Sodium, 钠 | mmol/L, mEq/L |
| 29 | `convert_soluble_transferrin_receptor_unit` | Soluble Transferrin Receptor, 可溶性转铁蛋白受体 | nmol/L, mg/L, mg/dL, mg/100mL, mg%, µg/mL |
| 30 | `convert_squamous_cell_carcinoma_unit` | Squamous cell carcinoma, 鳞状细胞癌 | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 31 | `convert_testosterone_unit` | Testosterone, 睾酮 | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 32 | `convert_theobromine_unit` | Theobromine, 茶碱 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 33 | `convert_threonine_thr_unit` | Threonine (Thr), 苏氨酸 (Thr) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 34 | `convert_coagulation_time_tt_unit` | Coagulation Time (TT), 凝血酶时间 (TT) | s, sec |
| 35 | `convert_thyroglobulin_tg_unit` | Thyroglobulin (Tg), 甲状腺球蛋白 (Tg) | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 36 | `convert_thyroid_uptake_unit` | Thyroid uptake, 甲状腺摄取 | Proportion of 1.0, % |
| 37 | `convert_total_t4_unit` | Thyroxine (Total T4), 甲状腺素(总 T4) | nmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL |
| 38 | `convert_free_thyroxine_ft4_unit` | Free Thyroxine (FT4), 游离甲状腺素(FT4) | pmol/L, ng/dL, ng/100mL, ng%, ng/mL, ng/L, pg/mL |
| 39 | `convert_thyroxine_binding_globulin_unit` | Thyroxine-Binding Globulin (TBG), 甲状腺素结合球蛋白 (TBG) | nmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 40 | `convert_tobramycin_unit` | Tobramycin, 妥布霉素 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 41 | `convert_total_protein_unit` | Total Protein, 总蛋白 | g/L, g/dL, g/100mL, g%, mg/mL |
| 42 | `convert_transferrin_unit` | Transferrin, 转铁蛋白 | µol/l, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 43 | `convert_triglycerides_unit` | Triglycerides, 甘油三酯 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 44 | `convert_triiodothyronine_t3_unit` | Triiodothyronine (T3), 三碘甲状腺原氨酸(T3) | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 45 | `convert_free_triiodothyronine_ft3_unit` | Free Triiodothyronine (FT3), 游离三碘甲状腺原氨酸(FT3) | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, ng/dL, ng/L |
| 46 | `convert_troponin_i_unit` | Troponin I (TnI), 肌钙蛋白 I (TnI) | ng/mL, µg/L, µg/dL, µg/1, µg%, µg/L |
| 47 | `convert_troponin_t_unit` | Troponin T (TnT), 肌钙蛋白 T (TnT) | ng/mL, µg/L, µg/dL, µg/1, µg%, µg/L |
| 48 | `convert_tryptophan_unit` | The English term for "色氨酸 (Trp)" is "Tryptophan"., 色氨酸 (Trp) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 49 | `convert_TSH_Thyroid_Stimulating_Hormone_unit` | TSH - Thyroid Stimulating Hormone, TSH - 促甲状腺激素 | µIU/mL, mIU/L |
| 50 | `convert_tyrosine_tyr_unit` | Tyrosine (Tyr), 酪氨酸(Tyr) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 51 | `convert_urea_unit` | Urea, 尿素 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 52 | `convert_blood_urea_nitrogen_unit` | Blood Urea Nitrogen (BUN), 尿素氮 (BUN) | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 53 | `convert_uric_acid_unit` | Uric Acid, 尿酸 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 54 | `convert_valine_val_unit` | Valine (Val), 缬氨酸(Val) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 55 | `convert_valproic_acid_unit` | Valproic acid, 丙戊酸 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 56 | `convert_vancomycin_unit` | Vancomycin, 万古霉素 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 57 | `convert_vitamin_b1_thiamine_unit` | Vitamin B1 (Thiamine), 维生素 B1(硫胺素) | nmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL |
| 58 | `convert_vitamin_b12_cobalamin_cyanocobalamin_unit` | Vitamin B12 (Cobalamin, Cyanocobalamin), 维生素 B12(钴胺素、氰钴胺素) | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 59 | `convert_vitamin_b3_niacin_nicotinic_acid_unit` | Vitamin B3 (Niacin, Nicotinic Acid), 维生素 B3(烟酸、烟酸) | ng/mL, µg/L, µg/dL, µg/100mL, µg%, µg/mL |
| 60 | `convert_vitamin_b6_pyridoxal_phosphate_unit` | Vitamin B6 (Pyridoxal Phosphate), 维生素 B6(磷酸吡哆醛) | nmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL |
| 61 | `convert_vitamin_c_ascorbic_acid_unit` | Vitamin C (Ascorbic Acid), 维生素 C(抗坏血酸) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 62 | `convert_vitamin_d_total_unit` | Vitamin D Total, 维生素 D 总量 | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 63 | `convert_vitamin_d_25_hydroxy_calcifediol_unit` | Vitamin D, 25-hydroxy (Calcifediol), 维生素 D，25-羟基(骨化二醇) | nmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 64 | `convert_vitamin_d3_125_dihydroxy_calcifediol_unit` | Vitamin D3, 1,25-dihydroxy (Calcifediol), 维生素 D3，1,25-二羟基(骨化三醇) | pmol/L, pg/mL, ng/L, ng/dL, ng/100mL, ng% |
| 65 | `convert_vitamin_E_alpha_tocopherol_unit` | Vitamin E (α-tocopherol), 维生素 E(α-生育酚) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 66 | `convert_vitamin_k_phylloquinone_unit` | Vitamin K (Phylloquinone), 维生素 K(叶绿醌) | nmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 67 | `convert_white_blood_cell_unit` | White Blood Cell (WBC), 白细胞 (WBC) | 10^9/L, G/L, Gpt/L, cells/L, 10^3/µL, 10^3/mm^3, K/µL, K/mm^3, cells/µL, cells/mm^3 |
| 68 | `convert_zinc_zn_unit` | Zinc (Zn), 锌 (Zn) | µmol/L, µg/mL, µg/dL, µg/100mL, µg%, µg/L, mg/L |
| 69 | `convert_insulin_like_growth_factor_binding_protein_3_unit` | Insulin-like Growth Factor Binding Protein 3 (IGFBP-3), 胰岛素样生长因子结合蛋白 3 (IGFBP-3) | µg/mL, µg/dL, µg/100mL, µg%, µg/L, mg/L |
| 70 | `convert_beta_hydroxybutyric_acid_unit` | β-Hydroxybutyric Acid, β-羟丁酸 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 71 | `convert_17_Hydroxyprogesterone_unit` | 17-Hydroxyprogesterone, 17-羟孕酮 | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 72 | `convert_paracetamol_unit` | Paracetamol, 对乙酰氨基酚 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 73 | `convert_acetoacetic_acid_acetoacetate_unit` | Acetoacetic acid (Acetoacetate), 乙酰乙酸(乙酰乙酸盐) | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 74 | `convert_acetone_unit` | Acetone, 丙酮 | mmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 75 | `convert_acid_phosphatase_unit` | Acid Phosphatase (ACP), 酸性磷酸酶 (ACP) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L)L, µmol/(h•mL) |
| 76 | `convert_activated_partial_thromboplastin_time_unit` | Activated Partial Thromboplastin Time (APTT), 活化部分凝血活酶时间 (APTT) | s, sec |
| 77 | `convert_adrenocorticotropic_hormone_unit` | Adrenocorticotropic Hormone (ACTH), 促肾上腺皮质激素 (ACTH) | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 78 | `convert_alanine_ala_unit` | Alanine (Ala), 丙氨酸(Ala) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/L |
| 79 | `convert_alanine_aminotransferase_ALT_SGPT_unit` | Alanine Aminotransferase (ALT/SGPT), 丙氨酸氨基转移酶 (ALT/SGPT) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 80 | `convert_albumin_unit` | Albumin, 白蛋白 | mmol/L, µmol/L, g/L, g/dL, g/100mL, g%, mg/mL |
| 81 | `convert_ethanol_dehydrogenase_adh_unit` | Ethanol Dehydrogenase (ADH), 乙醇脱氢酶(ADH) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 82 | `convert_aldehyde_dehydrogenase_unit` | Aldehyde dehydrogenase, 醛缩酶 | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 83 | `convert_aldosterone_unit` | Aldosterone, 醛固酮 | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, pg/mL |
| 84 | `convert_alkaline_phosphatase_ALP_unit` | Alkaline Phosphatase (ALP), 碱性磷酸酶 (ALP) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 85 | `convert_alpha1_acid_glycoprotein_unit` | α1-酸性糖蛋白, α1-酸性糖蛋白 | mmol/L, µmol/L, g/L, g/dL, g/100mL, g%, mg/mL |
| 86 | `convert_alpha_1_antitrypsin_unit` | Alpha-1 Antitrypsin, α1-抗胰蛋白酶 | mmol/L, µmol/L, g/L, g/dL, g/100mL, g%, mg/mL |
| 87 | `convert_alpha1_Microglobulin_unit` | α1-Microglobulin, α1‑微球蛋白 | µmol/L, nmol/L, mg/L, mg/dL, mg/100mL, mg%, µg/mL |
| 88 | `convert_AFP_AlphaFetoprotein_unit` | AFP (Alpha-fetoprotein), 甲胎蛋白(AFP) | IUmL, ng/mL, ng/dL, ng/100mL, ng%, µg/L |
| 89 | `convert_ammonia_nh3_unit` | Ammonia (NH3), 氨(NH3) | µmol/L, µg/dL, µg/100mL, µg%, µg/mL, µg/L, mg/L |
| 90 | `convert_amylase_unit` | Amylase, 淀粉酶 | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 91 | `convert_pancreatic_amylase_unit` | Pancreatic amylase, 胰淀粉酶 | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 92 | `convert_androstenedione_unit` | Androstenedione, 雄烯二酮 | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 93 | `convert_anti_thyroid_peroxidase_antibody_anti_tpo_unit` | Anti-Thyroid Peroxidase Antibody (Anti-TPO), 甲状腺过氧化物酶抗体(Anti-TPO) | IU/mL, kIU/L |
| 94 | `convert_TSH_Receptor_Antibody_Anti_TSHR_unit` | TSH Receptor Antibody (Anti-TSHR), TSH 受体抗体(Anti-TSHR) | IU/mL, kIU/L |
| 95 | `convert_anti_cyclic_citrullinated_peptide_antibody_unit` | Anti-Cyclic Citrullinated Peptide Antibody (Anti-CCP), 抗环瓜氨酸肽抗体(Anti-CCP) | U/mL, kU/L |
| 96 | `convert_anti_thyroglobulin_antibody_anti_tg_unit` | Anti-Thyroglobulin Antibody (Anti-Tg), 甲状腺球蛋白抗体 (Anti-Tg) | IU/mL, kIU/L |
| 97 | `convert_antidiuretic_hormone_vasopressin_unit` | Antidiuretic Hormone (Vasopressin), 抗利尿激素(血管加压素) | pmol/L, pg/mL, ng/L, ng/dL, ng/100mL, ng% |
| 98 | `convert_antistreptolysin_o_unit` | Antistreptolysin O (ASLO), 抗链球菌溶血素O(ASLO) | U/mL, kU/L, IU/mL, kIU/L |
| 99 | `convert_antithrombin_iii_activity_unit` | Antithrombin III activity, 抗凝血酶III活性 | Proportion, %, UmL, kU/L |
| 100 | `convert_anti_mullerian_hormone_unit` | Anti-Müllerian Hormone (AMH), 抗苗勒氏管激素(AMH) | pmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, pg/mL |
| 101 | `convert_apolipoprotein_A_1_unit` | Apolipoprotein A-1, 载脂蛋白A-1 | mmol/L, µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 102 | `convert_apolipoprotein_b_unit` | Apolipoprotein B, 载脂蛋白B | mmol/L, µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 103 | `convert_arginine_arg_unit` | Arginine (Arg), 精氨酸(Arg) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 104 | `convert_asparagine_asn_unit` | Asparagine (Asn), 天冬酰胺(Asn) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 105 | `convert_aspartate_aminotransferase_ast_sgot_unit` | Aspartate Aminotransferase (AST/SGOT), 天冬氨酸氨基转移酶(AST/SGOT) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 106 | `convert_aspartic_acid_asp_unit` | Aspartic Acid (Asp), 天冬氨酸(Asp) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 107 | `convert_basophil_absolute_value_unit` | Basophil (Basophil Absolute Value), 嗜碱性粒细胞(嗜碱性粒细胞绝对值) | 109/L, G/L, Gpt/L, cells/L, 103/µL, 103/mm3, k/µL, k/mm3, cells/µL, cells/mm3 |
| 108 | `convert_basophil_baso_unit` | Basophil (BASO), 嗜碱性粒细胞(BASO) | Proportion of 1.0, Fraction, % |
| 109 | `convert_beta_collagen_degradation_product_type_i_collagen_degradation_product_unit` | β-Collagen Degradation Product (Type I Collagen Degradation Product), β-胶原降解产物(Ⅰ型胶原降解产物) | ng/mL, ng/dL, ng/100mL, ng%, ng/L, pg/mL |
| 110 | `convert_beta2_microglobulin_unit` | β2-Microglobulin (β2-M), β2-微球蛋白 (β2-M) | nmol/L, mg/L, mg/dL, mg/100mL, mg%, µg/mL, ng/mL |
| 111 | `convert_bicarbonate_hco3_minus_unit` | Bicarbonate (HCO3-), 碳酸氢盐(HCO3-) | mmol/L, µmol/L, mEq/L, mg/dL, mg/100mL, mg%, µg/mL, mg/L |
| 112 | `convert_direct_bilirubin_unit` | Direct Bilirubin, 直接胆红素 | µmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 113 | `convert_total_bilirubin_unit` | Total Bilirubin, 总胆红素 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 114 | `convert_vitamin_b7_unit` | Biotin (Vitamin B7), 生物素(维生素B7) | nmol/L, pg/mL, ng/L, ng/dL, ng/100mL, ng% |
| 115 | `convert_c_peptide_unit` | C-peptide, C肽 | nmol/L, pmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 116 | `convert_c_reactive_protein_unit` | C-reactive protein (CRP), C-反应蛋白(CRP) | nmol/L, mg/L, mg/dL, mg/100mL, mg%, µg/mL, g/L |
| 117 | `convert_complement_factor_3_unit` | Complement Factor 3 (C3), 补体因子3(C3) | g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 118 | `convert_complement_factor_4_unit` | Complement Factor 4 (C4), 补体因子4(C4) | µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 119 | `convert_cancer_antigen_125_unit` | Cancer Antigen 125, 癌抗原 125 | U/mL, kU/L |
| 120 | `convert_cancer_antigen_15_3_unit` | Cancer Antigen 15-3, 癌抗原 15-3 | U/mL, kU/L |
| 121 | `convert_cancer_antigen_19_9_unit` | Cancer Antigen 19-9, 癌抗原 19-9 | U/mL, kU/L |
| 122 | `convert_cancer_antigen_72_4_unit` | Cancer Antigen 72-4, 癌抗原 72-4 | U/mL, kU/L |
| 123 | `convert_calcitonin_unit` | Calcitonin, 降钙素 | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 124 | `convert_calcium_unit` | Calcium, 钙 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL, mEq/l |
| 125 | `convert_carbamazepine_unit` | Carbamazepine, 卡马西平 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 126 | `convert_carcinoembryonic_antigen_cea_unit` | Carcinoembryonic Antigen (CEA), 癌胚抗原 | µg/L, ng/L, ng/dL, ng/100mL, ng%, ng/mL |
| 127 | `convert_ceruloplasmin_unit` | Ceruloplasmin, 铜蓝蛋白 | mmol/L, µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 128 | `convert_chloride_unit` | Chloride, 氯化物 | mmol/L, mEq/L |
| 129 | `convert_high_density_lipoprotein_cholesterol_unit` | High-density lipoprotein cholesterol, 高密度脂蛋白胆固醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 130 | `convert_low_density_lipoprotein_cholesterol_unit` | Low-density lipoprotein cholesterol, 低密度脂蛋白胆固醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 131 | `convert_total_cholesterol_unit` | Total Cholesterol, 总胆固醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 132 | `convert_choline_esterase_unit` | Choline Esterase, 胆碱酯酶 | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 133 | `convert_ck_mb_mass_unit` | CK-MB Mass (Quantitative Detection), CK-MB质量(定量检测) | µg/L, ng/L, ng/mL, ng/dL, ng/100mL, ng% |
| 134 | `convert_copper_unit` | Copper, 铜 | µmol/L, µg/mL, µg/dL, µg/100mL, ng%, µg/L, mg/L |
| 135 | `convert_cortisol_unit` | Cortisol, 皮质醇 | nmol/L, µg/dL, µg/100mL, ng%, µg/L, mg/L |
| 136 | `convert_creatine_kinase_unit` | Creatine Kinase, 肌酸激酶 | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 137 | `convert_ck_mb_activity_unit` | CK-MB(活性), CK-MB(活性) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 138 | `convert_creatinine_unit` | Creatinine, 肌酐 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 139 | `convert_cellular_keratin_19_fragment_unit` | Cellular Keratin 19 Fragment, 细胞角蛋白19片段 | µg/mL, µg/dL, µg/100mL, ng%, ng/mL |
| 140 | `convert_cystatin_c_unit` | Cystatin C, 胱抑素C | mg/L, mg/dL, mg/100mL, mg%, µg/mL |
| 141 | `convert_cysteine_unit` | Cysteine, 半胱氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 142 | `convert_cystine_unit` | Cystine, 胱氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 143 | `convert_D_dimer_unit` | D-dimer, D-二聚体 | mg FEU/L, mg/L (DDU), µg/L (DDU), µg FEU/mL, ng FEU/mL, µg/mL (DDU), ng/mL (DDU) |
| 144 | `convert_dehydroepiandrosterone_sulfate_unit` | Dehydroepiandrosterone sulfate, 硫酸脱氢表雄酮 | µmol/L, µg/mL, µg/dL, µg/100mL, µg%, µg/L, mg/L |
| 145 | `convert_digitalis_toxin_unit` | Digitalis Toxin, 毛地黄毒苷 | nmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 146 | `convert_digoxin_unit` | Digoxin, 地高辛 | nmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 147 | `convert_eosinophil_cationic_protein_unit` | Eosinophil cationic protein, 嗜酸性粒细胞阳离子蛋白 | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 148 | `convert_eosinophil_absolute_count_unit` | Eosinophil (Eosinophil Absolute Count), 嗜酸性粒细胞(嗜酸性粒细胞绝对计数) | 10^9/L, G/L, Gpt/L, cells/L, 10^3/µL, 10^3/mm^3, K/µL, K/mm^3, cells/µL, cells/mm^3 |
| 149 | `convert_eosinophil_unit` | Eosinophil, 嗜酸性粒细胞 | Proportion of 1.0, Fraction, % |
| 150 | `convert_erythropoietin_unit` | Erythropoietin, 促红细胞生成素 | mIU/mL, IU/L |
| 151 | `convert_estradiol_unit` | Estradiol, 雌二醇 | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 152 | `convert_free_estradiol_unit` | Free Estradiol, 游离雌三醇 | mmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 153 | `convert_estrone_unit` | Estrone, 雌酮 | pmol/L, ng/dL, ng/100mL, ng%, ng/L, pg/mL |
| 154 | `convert_ethanol_unit` | Ethanol, 乙醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 155 | `convert_ethylene_glycol_unit` | Ethylene glycol, 乙二醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 156 | `convert_ferritin_unit` | Ferritin, 铁蛋白 | nmol/L, pmol/L, µg/L, µg/dL, µg/100mL, µg%, ng/mL |
| 157 | `convert_fibrinogen_unit` | Fibrinogen, 纤维蛋白原 | g/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 158 | `convert_folic_acid_unit` | Folic Acid, 叶酸盐 | nmol/L, pmol/L, ng/mL, ng/dL, ng/100mL, ng%, µg/L |
| 159 | `convert_folic_acid_unit` | Folic Acid, 叶酸 | nmol/L, pmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 160 | `convert_follicle_stimulating_hormone_unit` | Follicle-stimulating hormone (FSH), 卵泡刺激素 (FSH) | mIU/mL, IU/L |
| 161 | `convert_free_human_chorionic_gonadotropin_beta_subunit_unit` | Free Human Chorionic Gonadotropin Beta Subunit (Free βhCG), 游离人绒毛膜促性腺激素β亚基(游离βhCG) | ng/mL, mIU/mL, IU/L |
| 162 | `convert_fructosamine_unit` | Fructosamine, 果糖胺 | mmol/L, µmol/L |
| 163 | `convert_fructose_unit` | Fructose, 果糖 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 164 | `convert_galactose_unit` | Galactose, 半乳糖 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 165 | `convert_gamma_glutamyltransferase_unit` | Gamma-glutamyltransferase (GGT), γ-谷氨酰转肽酶(GGT) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 166 | `convert_gastrin_unit` | Gastrin, 胃泌素 | pmol/L, pg/mL, ng/L, ng/dL, ng/100mL, ng%, mU/L |
| 167 | `convert_gentamicin_unit` | Gentamicin, 庆大霉素 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 168 | `convert_glucagon_unit` | Glucagon, 胰高血糖素 | ng/L, pg/mL, ng/dL, ng/100mL, ng% |
| 169 | `convert_glucose_unit` | Glucose, 葡萄糖 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 170 | `convert_glutamate_dehydrogenase_gldh_unit` | Glutamate Dehydrogenase (GLDH), 谷氨酸脱氢酶 (GLDH) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 171 | `convert_glutamic_acid_glu_unit` | Glutamic Acid (Glu), 谷氨酸(Glu) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 172 | `convert_glutamine_gln_unit` | Glutamine (Gln), 谷氨酰胺 (Gln) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 173 | `convert_glycine_gly_unit` | Glycine (Gly), 甘氨酸(Gly) | mmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 174 | `convert_growth_differentiation_factor_15_unit` | Growth Differentiation Factor-15 (GDF-15), 生长分化因子-15 (GDF-15) | pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 175 | `convert_globulin_unit` | Globulin, 结合珠蛋白 | µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 176 | `convert_human_epididymis_protein_4_unit` | Human Epididymis Protein 4 (HE4), 人附睾蛋白4(HE4) | nmol/L, pmol/L |
| 177 | `convert_hematocrit_hct_unit` | Hematocrit (HCT), 血细胞比容(HCT) | L/L, Proportion of 1.0, volume fraction, % |
| 178 | `convert_hemoglobin_hgb_unit` | Hemoglobin (HGB), 血红蛋白 (HGB) | g/L, g/dL, g/100mL, g%, mg/mL |
| 179 | `convert_hemoglobin_subunit_unit` | Hemoglobin Subunit, 血红蛋白单体(亚基) | mmol/L, µmol/L, g/L, g/dL, g/100mL, g%, mg/mL |
| 180 | `convert_hemoglobin_tetramer_unit` | Hemoglobin Tetramer, 血红蛋白四聚体 | mmol/L, µmol/L, g/L, g/dL, g/100mL, g%, mg/mL |
| 181 | `convert_histidine_his_unit` | Histidine (His), 组氨酸(His) | mmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 182 | `convert_homocysteine_hcy_unit` | Homocysteine (HCY), 同型半胱氨酸 (HCY) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 183 | `convert_human_chorionic_gonadotropin_unit` | Human Chorionic Gonadotropin (hCG), 人绒毛膜促性腺激素 (hCG) | mIU/mL, IU/L |
| 184 | `convert_human_growth_hormone_unit` | Human Growth Hormone (hGH), 人类生长激素(hGH) | mIU/L, ng/mL, ng/dL, ng/100mL, ng%, µg/L |
| 185 | `convert_insulin_like_growth_factor_1_unit` | Insulin-like Growth Factor 1 (IGF-1), 胰岛素样生长因子1(IGF-1) | nmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 186 | `convert_immunoglobulin_a_unit` | Immunoglobulin A (IgA), 免疫球蛋白 A (IgA) | µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 187 | `convert_immunoglobulin_e_unit` | Immunoglobulin E (IgE), 免疫球蛋白 E (IgE) | IU/mL, ng/mL, ng/dL, ng/100mL, ng%, µg/L |
| 188 | `convert_immunoglobulin_g_unit` | Immunoglobulin G (IgG), 免疫球蛋白 G (IgG) | µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 189 | `convert_immunoglobulin_m_unit` | Immunoglobulin M (IgM), 免疫球蛋白 M (IgM) | µmol/L, g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 190 | `convert_insulin_unit` | Insulin, 胰岛素 | pmol/L, µIU/mL, mIU/L |
| 191 | `convert_interleukin_6_unit` | Interleukin-6 (IL-6), 白细胞介素-6 (IL-6) | pg/mL, pg/dL, pg/100mL, µg%, pg/L, ng/L |
| 192 | `convert_iron_fe_unit` | Iron (Fe), 铁(Fe) | µmol/L, mmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL, mg/L |
| 193 | `convert_total_iron_binding_capacity_unit` | Total Iron Binding Capacity (TIBC), 总铁结合力 (TIBC) | µmol/L, mmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL, mg/L |
| 194 | `convert_unsaturated_iron_binding_capacity_unit` | Unsaturated Iron Binding Capacity (UIBC), 不饱和铁结合力(UIBC) | µmol/L, mmol/L, µg/dL, µg/100mL, µg%, µg/L, ng/mL, mg/L |
| 195 | `convert_isoleucine_ile_unit` | Isoleucine (Ile), 异亮氨酸(Ile) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 196 | `convert_isopropyl_alcohol_unit` | Isopropyl alcohol, 异丙醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 197 | `convert_kappa_light_chain_unit` | κ light chain, κ轻链 | g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 198 | `convert_lactic_acid_unit` | Lactic Acid, 乳酸 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 199 | `convert_lactate_dehydrogenase_unit` | Lactate Dehydrogenase (LDH), 乳酸脱氢酶 (LDH) | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 200 | `convert_lambda_light_chain_unit` | λ light chain, λ轻链 | g/L, mg/dL, mg/100mL, mg%, mg/mL |
| 201 | `convert_leucine_leu_unit` | Leucine (Leu), 亮氨酸 (Leu) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 202 | `convert_lidocaine_unit` | Lidocaine, 利多卡因 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 203 | `convert_lipase_unit` | Lipase, 脂肪酶 | nkat/L, µkat/L, nmol/(s•L), µmol/(s•L), U/L, IU/L, µmol/(min•L), µmol/(h•L), µmol/(h•mL) |
| 204 | `convert_lipopolysaccharide_binding_protein_unit` | Lipopolysaccharide-binding protein (LBP), 脂多糖结合蛋白 (LBP) | µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 205 | `convert_lipoprotein_a_unit` | Lipoprotein(a), 脂蛋白(a) | g/L, mg/L, mg/dL, mg/100mL, mg%, mg/mL |
| 206 | `convert_lithium_Li_unit` | Lithium (Li), 锂 (Li) | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL, mEq/l |
| 207 | `convert_luteinizing_hormone_unit` | Luteinizing Hormone (LH), 黄体生成素 (LH) | mIU/mL, IU/L |
| 208 | `convert_lymphocyte_absolute_count_unit` | Lymphocyte (Lymphocyte Absolute Count), 淋巴细胞(淋巴细胞绝对计数) | 10^9/L, G/L, Gpt/L, cells/L, 10^3/µL, 10^3/mm^3, K/µL, K/mm^3, cells/µL, cells/mm^3 |
| 209 | `convert_lymphocyte_unit` | Lymphocyte, 淋巴细胞 (LYMPH) | Proportion of 1.0, Fraction, % |
| 210 | `convert_lysine_unit` | Lysine, 赖氨酸 | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 211 | `convert_macroprolactinemia_unit` | Macroprolactinemia, 巨泌乳素 | Fraction, % |
| 212 | `convert_magnesium_unit` | Magnesium, 镁 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL, mEg/L |
| 213 | `convert_mean_corpuscular_hemoglobin_concentration_unit` | Mean Corpuscular Hemoglobin Concentration (MCHC), 平均红细胞血红蛋白含量 | fmol, fmol/cell, pg, pg/cell |
| 214 | `convert_mean_corpuscular_hemoglobin_concentration_unit` | Mean Corpuscular Hemoglobin Concentration (MCHC), 平均红细胞血红蛋白浓度 | mmol/L, µmol/L, mg/L, mg/dL, mg/100mL, mg%, mg/mL, % |
| 215 | `convert_mean_corpuscular_volume_unit` | Mean Corpuscular Volume (MCV), 平均红细胞体积 | fL, µm^3, cu µm, cubic µm |
| 216 | `convert_methanol_unit` | Methanol, 甲醇 | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 217 | `convert_methionine_met_unit` | Methionine (Met), 蛋氨酸(Met) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 218 | `convert_absolute_monocyte_count_unit` | Monocyte (Absolute Monocyte Count), 单核细胞(绝对单核细胞计数) | 10^9/L, G/L, Gpt/L, cells/L, 10^3/µL, 10^3/mm^3, K/µL, K/mm^3, cells/µL, cells/mm^3 |
| 219 | `convert_monocyte_unit` | Monocyte, 单核细胞 | Proportion of 1.0, Fraction, % |
| 220 | `convert_mean_platelet_volume_unit` | Mean Platelet Volume, 平均血小板体积 | fL, µm^3, cu µm, cubic µm |
| 221 | `convert_myoglobin_unit` | Myoglobin, 肌红蛋白 | nmol/L, ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 222 | `convert_N1_Methylnicotinamide_Nicotinic_Acid_Metabolite_unit` | N1-Methylnicotinamide (Nicotinic Acid Metabolite), N1-甲基烟酰胺(烟酸代谢物) | nmol/L, ng/mL, µg/L, µg/dL, µg/100mL, µg% |
| 223 | `convert_neuro_specific_enolase_unit` | Neuro-specific enolase (NSE), 神经元特异性烯醇化酶 (NSE) | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 224 | `convert_neutrophil_absolute_value_unit` | Neutrophil (Neutrophil Absolute Value), 中性粒细胞(中性粒细胞绝对值) | 10^9/L, G/L, Gpt/L, cells/L, 10^3/µL, 10^3/mm^3, K/µL, K/mm^3, cells/µL, cells/mm^3 |
| 225 | `convert_neutrophil_unit` | Neutrophil, 中性粒细胞(NEUT) | Proportion of 1.0, Fraction, % |
| 226 | `convert_n_terminal_pro_b_type_natriuretic_peptide_unit` | N-terminal pro-B-type natriuretic peptide (NT-proBNP), N末端B型利钠肽原(NT-proBNP) | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 227 | `convert_n_acetylprocainamide_napa_unit` | N-Acetylprocainamide (NAPA), N-乙酰普鲁卡因酰胺(NAPA) | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 228 | `convert_bone_calcification_ocn_unit` | Bone Calcification (OCN), 骨钙素(OCN) | ng/mL, ng/dL, ng/100mL, ng%, ng/L, µg/L |
| 229 | `convert_total_type_i_collagen_amino_terminal_extension_peptide_tp1np_unit` | Total Type I Collagen Amino-Terminal Extension Peptide (TP1NP), 总Ⅰ型前胶原氨基端延长肽(TP1NP) | ng/mL, ng/dL, ng/100mL, ng%, µg/L |
| 230 | `convert_pantothenic_acid_vitamin_b5_unit` | Pantothenic Acid (Vitamin B5), 泛酸(维生素 B5) | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 231 | `convert_parathyroid_hormone_pth_unit` | Parathyroid Hormone (PTH), 甲状旁腺激素(PTH) | pmol/L, pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
| 232 | `convert_phenobarbital_unit` | Phenobarbital, 苯巴比妥 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 233 | `convert_phenylalanine_phe_unit` | Phenylalanine (Phe), 苯丙氨酸(phe) | µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 234 | `convert_phenytoin_unit` | Phenytoin, 苯妥英 | µmol/L, µg/mL, mg/L, mg/dL, mg/100mL, mg% |
| 235 | `convert_phosphorus_p_unit` | Phosphorus (P), 磷 (P) | mmol/L, µmol/L, mg/dL, mg/100mL, mg%, mg/L, µg/mL |
| 236 | `convert_platelet_unit` | Platelet, 血小板(血小板) | 109/L, G/L, Gpt/L, cells/L, 103/µL, 103/mm3, K/µL, K/mm3, cells/µL, cells/mm3 |
| 237 | `convert_placental_growth_factor_unit` | Placental Growth Factor (PIGF), 胎盘生长因子(PIGF) | pg/mL, pg/dL, pg/100mL, pg%, pg/L, ng/L |
