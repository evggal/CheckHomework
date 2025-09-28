import { Link } from "react-router";

const MainPage = () => {
  return (
    <div>
      <p>Главная страница. Пока тут пусто</p>
      <Link to="/checkSolution" style={{padding:"10px 20px", border:"1px solid #000"}}>
        Страница проверки
      </Link>
      <Link to="/correctAndRecognizedSolution" style={{padding:"10px 20px", border:"1px solid #000"}}>
        Корректное-рапознанное решение
      </Link>
    </div>
  )
}

export default MainPage;
