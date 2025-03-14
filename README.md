Authors:
Thavas Antonio, Sevir Deliker
# Elora Neurotechnology Project

> **Empowering mental health diagnostics with EEG and AI**  

Elora is an innovative neurotechnology solution leveraging EEG brainwave analysis and machine learning to help doctors predict and understand emotional states in veterans. By combining cutting-edge AI with real-time EEG data, Elora aims to make mental health assessments more precise and personalized.

---

## ⭐ Overview  
Veterans struggling with PTSD and stress can often find it challenging to communicate their emotions. **Elora** provides an objective, data-driven assessment that supports clinicians in diagnosing and monitoring mental health conditions more accurately.

---

## 🚀 How It Works

### 1. Data Collection  
- **Muse 2 Headset**  
  - Records EEG signals at four sensor sites: `TP9, AF7, AF8, TP10`.  
  - Captures `Delta, Theta, Alpha, Beta, Gamma` wave activity.  
- **Multimodal Integration** (Optional)  
  - Links structural MRI data with EEG patterns for a comprehensive neuroimaging approach.

### 2. Machine Learning Model  
- **CNN + RNN Fusion**  
  - Fine-tuned on university patient datasets and validated clinical EEG records.  
  - Learns correlations between spectral EEG features and annotated emotional responses.
- **Transfer Learning & Real-Time Calibration**  
  - Model refines its predictions with new data, adapting on the fly.

### 3. Outputs & Insights  
- **Emotion Prediction**  
  - Dynamically visualizes user (veteran) emotional states for clinical review.  
- **Data Storage**  
  - Saves anxiety scores and diagnostic labels to Firebase for ongoing doctor access and monitoring.


---

# Tumor Types, Brain Waves, and Biological Implications

Below is a quick reference table mapping various tumor types to their characteristic EEG findings and the associated biological/clinical context (the “bio side”). These correlations are not absolute but provide general patterns often observed in neurological examinations and imaging studies.

| **Tumor Type**              | **Brain Wave Patterns**          | **Linked To**                                                                    | **Bio Side (Biological/Clinical Implications)**                                                                                                                                                                 |
|-----------------------------|----------------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Large Cell Carcinoma** <br>*(CT Scans)*        | High Delta Waves                           | Brain metastases, impaired brain activity                                        | - Originates often in the lungs; brain metastases can disrupt normal neuronal communication. <br>- High delta waves in EEG suggest slower cortical activity, often reflecting severe dysfunction or structural lesions in the cortex.                  |
| **Squamous Cell Carcinoma** <br>*(CT Scans)*     | High Theta & Delta Waves                  | Central nervous system involvement, brain function changes                       | - Commonly arises from epithelial cells (e.g. head and neck or lungs), can metastasize to the brain. <br>- High theta and delta indicate slowed cortical rhythms, often pointing to lesions or compromised brain tissue integrity.                       |
| **Glioma** <br>*(MRI Scans)*                    | High Delta & Theta Waves                  | Disrupted brain function, focal slow-wave activity                               | - Originates from glial cells (astrocytes, oligodendrocytes, or ependymal cells). <br>- Slow-wave patterns in EEG reflect local infiltration of tumor cells, causing edema or structural changes in brain tissue.                                      |
| **Meningioma** <br>*(MRI Scans)*                | High Delta Waves                           | Brain tissue compression, increased delta wave activity                          | - Arises from the meninges (protective layers around the brain/spinal cord). <br>- Can compress adjacent brain tissue, leading to focal neurological deficits and slow-wave activity where the cortex is distorted or displaced.                        |
| **Pituitary Tumors** <br>*(MRI Scans)*          | High Theta Waves                           | Altered brain rhythms, hormonal & sleep regulation impact                        | - Located in the pituitary gland, can affect hormonal balance (e.g. cortisol, growth hormone), potentially altering sleep and circadian rhythms. <br>- High theta waves can correlate with deeper or dysregulated thalamocortical activity.             |
| **Brain Wave: High Delta & Theta** <br>*(General Pattern)* | High Delta & Theta Waves (combined)        | Brain metastasis, reduced cortical function                                      | - Often indicates significant slowing of activity in the cortex. <br>- Delta (1-4 Hz) and Theta (4-8 Hz) waves typically appear in severe brain dysfunction, sedation states, or focal lesions.                                                      |

## Key Takeaways

1. **High Delta Waves**: Commonly associated with more severe or focal cortical dysfunction. Tumors creating pressure or infiltrating the brain often produce delta activity in nearby regions.
2. **High Theta Waves**: Often indicative of reduced alertness or early-stage cortical slowing. Can be seen when tumors affect subcortical areas or disrupt normal thalamocortical loops.
3. **Imaging Correlation**: CT scans are typically used to identify metastases or large structural lesions. MRI is more detailed for soft tissue differentiation (e.g., gliomas, meningiomas, pituitary tumors).
4. **Clinical Relevance**: These EEG wave patterns, combined with imaging data (CT/MRI) and clinical exams, guide diagnosis and treatment. Slower wave activity often signals the need for further investigation into structural lesions, edema, or mass effect.

---

## 🌱 Potential Applications
1. **Veteran Mental Health Diagnostics**  
   - Helps evaluate PTSD, depression, and other stress-related conditions.  
2. **AI-Powered Neurotherapy**  
   - Facilitates targeted emotional regulation exercises tailored to individual needs.  
3. **Cognitive & Affective Neuroscience Research**  
   - Contributes to the broader scientific understanding of EEG-emotion correlations.

---

## 📌 Why Elora?
- **Objectivity** – Shifts from self-reporting to direct neurophysiological measurements.  
- **Precision** – Harnesses deep learning for accurate emotional state predictions.  
- **Scalability** – Integrates seamlessly into clinical and telemedicine workflows.

---

## 💡 Conclusion
Elora combines **computational neuropsychiatry**, **AI**, and **biometric analytics** to offer a next-generation approach to mental health evaluation. By capitalizing on EEG signal processing and deep learning, it sets the stage for **precision neurotherapeutics** and novel cognitive AI research, improving outcomes for veterans and advancing neuroscience.

---

### 👀 Want to Contribute?
1. **Fork this repo** to explore the code.  
2. Submit **pull requests** or open issues to help improve Elora.  
3. Spread the word and help transform mental health care!

**Stay Brainy & Keep Building!** 🧠✨
