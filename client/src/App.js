import React, {useState, useEffect} from 'react'

function App() {
  //data is data, setData help manipulate that data
  //in this context, setData is used to fetch data from the backend
  const [data, setData] = useState([{}])

  useEffect(() => {
    //fetches members route in server.py
    fetch("/members").then(
      //whatever is fetched(res) will be stored in a json
      res => res.json()
    ).then(
      data => {
        //whatever data is inside the json will be stored in data using setData. Then we log it
        setData(data)
        console.log(data)
      }
    )
  })
  return (
    <div>
      {(typeof data.members === 'undefined') ? (
        <p>Loading...</p>
      ): (
        data.members.map((member, i) => (
          <p key ={i}>{member}</p>
        ))
      )}
    </div>
  )
}

export default App
