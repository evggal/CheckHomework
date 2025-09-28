import { Link } from "react-router";
import CardImage from "../../elements/cardImage/CardImage";

const CorrectAndRecognizedSolutionPage = () => {
  return (
    <div>
       <p>Сравнение эталонного решения с распознанным</p>
        <Link to="/" style={{padding:"10px 20px", border:"1px solid #000"}}>
            На главную
        </Link>
        <Link to="/checkSolution" style={{padding:"10px 20px", border:"1px solid #000"}}>
          Страница проверки
        </Link>
        {/* Эталонное решение и распознанное решение */}
        <CardImage /> 
        <CardImage />
    </div>
  )
}

export default CorrectAndRecognizedSolutionPage;
