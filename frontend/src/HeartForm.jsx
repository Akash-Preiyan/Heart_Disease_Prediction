import { useState } from "react";
import axios from "axios";

const getOptionsForField = (key) => {
  const options = {
    sex: [["Male", 1], ["Female", 0]],
    cp: [
      ["Typical Angina", 0],
      ["Atypical Angina", 1],
      ["Non-anginal Pain", 2],
      ["Asymptomatic", 3],
    ],
    fbs: [["True", 1], ["False", 0]],
    restecg: [
      ["Normal", 0],
      ["ST-T Abnormality", 1],
      ["Left Ventricular Hypertrophy", 2],
    ],
    exang: [["Yes", 1], ["No", 0]],
    slope: [["Upsloping", 0], ["Flat", 1], ["Downsloping", 2]],
    ca: [["0", 0], ["1", 1], ["2", 2], ["3", 3]],
    thal: [["Normal", 1], ["Fixed Defect", 2], ["Reversible Defect", 3]],
  };
  return options[key] || [];
};

export default function HeartForm() {
  const defaultFormData = {
    age: "",
    sex: "",
    cp: "",
    trestbps: "",
    chol: "",
    fbs: "",
    restecg: "",
    thalach: "",
    exang: "",
    oldpeak: "",
    slope: "",
    ca: "",
    thal: "",
  };
  const [prediction, setPrediction] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState(defaultFormData);

  const handleChange =  (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();


    try {
      const response = await axios.post("http://localhost:8000/predict", formData);
      const result = response.data.prediction === 1 ? "Positive" : "Negative";
      setPrediction(result);
      setSubmitted(true);
    } catch (error) {
      console.error("Error sending data: ", error)
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-transparent border-black p-2 rounded-xl shadow-xl w-screen h-[100%] gap-1"
    >
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {Object.entries(formData).map(([key, val]) => (
          <div key={key} className="flex flex-col ">
            <label className="capitalize text-black font-sans">{key}</label>
            {["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"].includes(key) ? (
              <select
                name={key}
                value={val}
                onChange={handleChange}
                className="mt-1 p-1 border-4 border-black rounded-lg"
                required
              >
                <option value="">Select {key}</option>
                {getOptionsForField(key).map(([label, value]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="number"
                name={key}
                value={val}
                onChange={handleChange}
                placeholder={`Enter ${key}`}
                className=" border-black border-4 rounded-lg"
                required
              />
            )}
          </div>
        ))}
      </div>
      
      <div className="flex justify-center gap-2">
        <button
          type="submit"
          className={`w-sm mt-2  bg-red-400 text-black py-2 rounded-lg hover:bg-red-700 transition`}
        >
          {submitted ? `Result: ${prediction}` : "Predict"}
        </button>
        {submitted ? <button onClick={() => {
          setFormData(defaultFormData)
          setPrediction(null)
          setSubmitted(false)
        }} className="bg-black text-white w-[10%] mt-2 rounded-lg">Predict Again</button> : <></>}
      </div>
      
    </form>
  );
}
