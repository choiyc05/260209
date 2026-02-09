import { useState } from 'react'
import axios from "axios"

function App() {
  const [token, setToken] = useState("")
  const event1 = e => {
    e.preventDefault()
    console.log("코드 발급", e.target.email.value)
    axios.post(import.meta.env.VITE_APP_FASTAPI_LOGIN, {"email":e.target.email.value})
      .then(res=>{
        if (res.data.status) {
        // console.log(res)
        e.target.email.value=""
        alert("Email 발급이 완료되었습니다.")
        } else alert("입력하신 Email은 존재하지 않습니다.")
      })
      .catch(err=>console.log(err))
  }
  const event2 = e => {
    e.preventDefault()
    console.log("토큰 발급", e.target.code.value)
    axios.post(import.meta.env.VITE_APP_FASTAPI_CODE, {"id":e.target.code.value})
      .then(res=>{
        // console.log(res)
        if (res.data.status) {
        e.target.code.value=""
        setToken(res.data.access_token)
        alert("토큰 발행이 완료됐습니다.")
        } else alert("code가 유효하지 않습니다.")
      })
      .catch(err=>console.log(err))
  }
  const event3 = () => {
    console.log("사용자 정보 요청")
    axios.post(import.meta.env.VITE_APP_FASTAPI_ME, {}, 
      {headers:{"Authorization" : `Bearer ${token}`} }
      )
      .then(res=>console.log(res.data))
      .catch(err=>console.log(err))

  }

  return (
    <>
      <form onSubmit={event1}>
        <input type='email' name="email" required autoComplete='off' style={{"flex":"1"}} />
        <button type='submit'>코드 발급</button>
      </form>
      <hr/>
      <form onSubmit={event2}>
        <input type='text' name='code' required autoComplete='off' style={{"flex":"1"}} />
        <button type='submit'>토큰 발급</button>
      </form>
      <hr/>
      <button type='button' onClick={event3} style={{"width":"100%","cursor":"pointer"}}>사용자 정보</button>
    </>
  )
}

export default App
