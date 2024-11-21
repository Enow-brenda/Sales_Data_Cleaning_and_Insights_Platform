import { useState } from "react";


const cleanURL = "http://192.168.10.18:5000/";
const getDataURL = "http://192.168.10.18:5000/getOtherData";
#here am using the ip adress of my network since am using different users


function App() {
  // onchange states
  const [excelFile, setExcelFile] = useState(null);
  const [typeError, setTypeError] = useState(null);
  const [salesInsight,setSalesInsight]=useState("");

  // submit state
  const [excelData, setExcelData] = useState(null);

  // onchange event
  const handleFile = (e) => {
    let fileTypes = [
      "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "text/csv",
    ];
    let selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile && fileTypes.includes(selectedFile.type)) {
        setTypeError(null);
        let reader = new FileReader();
        reader.readAsArrayBuffer(selectedFile);
        reader.onload = (e) => {
          setExcelFile(e.target.result);
        };
      } else {
        setTypeError("Please select only csv file types");
        setExcelFile(null);
      }
    } else {
      console.log("Please select your file");
    }
  };

  // submit event
  const handleFileSubmit = async(e) => {
    e.preventDefault();
    if (excelFile !== null) {
      const formData = new FormData();
      formData.append('file', excelFile);
      try {
        const response = await fetch(cleanURL, {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();
        setExcelData(result.slice(0, 10));
        getSalesInsight();
        console.log('Success:', result);
      } catch (error) {
        console.error('Error:', error);
      }
       
     
    }
  };
  const getSalesInsight = async() => {
   
      try {
        const newFile="./../cleaned_files/new_"+excelFile
        const response = await fetch(getDataURL+"?filename="+newFile, {
          method: 'GET',
        })

        const result = await response.json();
        setSalesInsight(result);
        console.log('Success:', result);
      } catch (error) {
        console.error('Error:', error);
      }
      
    }
  

  return (
    <div className="wrapper">
      <h3>Sales Data Cleaning and Insights Platform</h3>

      {/* form */}
      <form className="form-group custom-form" onSubmit={handleFileSubmit}>
        <input
          type="file"
          className="form-control"
          required
          onChange={handleFile}
        />
        <button type="submit" className="btn btn-success btn-md">
          CLEAN FILE
        </button>
        {typeError && (
          <div className="alert alert-danger" role="alert">
            {typeError}
          </div>
        )}
      </form>

      {/* view data */}
      <div className="viewer">
        {excelData ? (<>
        <button type="submit" className="btn btn-success btn-md">
          DOWNLOAD NEW FILE
        </button>
    
        <h3>Some Analytics Related to this File:</h3>
        <p>{salesInsight}</p>
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  {Object.keys(excelData[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {excelData.map((individualExcelData, index) => (
                  <tr key={index}>
                    {Object.keys(individualExcelData).map((key) => (
                      <td key={key}>{individualExcelData[key]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>) : (
          <div>No Csv File is uploaded yet!</div>
      )}
      </div>
    </div>
  )
}

export default App;
