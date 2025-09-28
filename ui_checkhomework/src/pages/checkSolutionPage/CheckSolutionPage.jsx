import { Link } from "react-router";
import CardCheckInfo from "../../elements/cardCheckInfo/CardCheckInfo";
import CardImage from "../../elements/cardImage/CardImage";

const CheckSolutionPage = () => {
  return (
    <div>
        <p>
            Тут основная страница проверки
        </p>
        <Link to="/" style={{padding:"10px 20px", border:"1px solid #000"}}>
            На главную
        </Link>
        <Link to="/correctAndRecognizedSolution" style={{padding:"10px 20px", border:"1px solid #000"}}>
        Корректное-рапознанное решение
        </Link>
        {/*
        Элемнет - изображение
        Элемент - карточка
        */}
        <CardImage />
        <CardCheckInfo />
    </div>
  )
}

export default CheckSolutionPage;
