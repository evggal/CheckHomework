import { Link } from "react-router";
import CardCheckInfo from "../../elements/cardCheckInfo/CardCheckInfo";
import CardImage from "../../elements/cardImage/CardImage";
import matrix1 from '../../images/matrix_1.jpg'

const CheckSolutionPage = () => {
  return (
    <div style={{
      padding:'10px',
      display:'flex',
      gap:'20px',
      alignItems:'center',
      justifyContent:'center'
    }}>
        {/*<p>
            Тут основная страница проверки
        </p>
        <Link to="/" style={{padding:"10px 20px", border:"1px solid #000"}}>
            На главную
        </Link>
        <Link to="/correctAndRecognizedSolution" style={{padding:"10px 20px", border:"1px solid #000"}}>
        Корректное-рапознанное решение
        </Link>*/}
        {/*
        Элемнет - изображение
        Элемент - карточка
        */}
        <CardImage img={matrix1} style={{
          width:'60vw',
          height:'95vh'
          
        }} />
       
        <CardCheckInfo
          style={{ width: "25vw", height: "95vh" }}
          student="Иванов И. И."
          variant="22"
          task="2"
          img={matrix1}
          recognizedImg={matrix1} // можно заменить на другое изображение
        />

    </div>
  )
}

export default CheckSolutionPage;
