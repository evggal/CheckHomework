import { Link } from "react-router";
import CardImage from "../../elements/cardImage/CardImage";
import matrix1 from '../../images/matrix_1.jpg'
import matrix2 from '../../images/matrix_2.jpg'

const CorrectAndRecognizedSolutionPage = () => {
  return (
    <div style={{
      padding:'10px',
      display:'flex',
      gap:'20px',
      alignItems:'center',
      justifyContent:'center'
    }}>
       {/*<p>Сравнение эталонного решения с распознанным</p>
        <Link to="/" style={{padding:"10px 20px", border:"1px solid #000"}}>
            На главную
        </Link>
        <Link to="/checkSolution" style={{padding:"10px 20px", border:"1px solid #000"}}>
          Страница проверки
        </Link>*/}
        {/* Эталонное решение и распознанное решение */}
        <CardImage img={matrix1} style={{
                  width:'50vw',
                  height:'95vh'
                  
                }}  /> 
        <CardImage img={matrix2} style={{
                  width:'50vw',
                  height:'95vh'
                  
                }}  />
    </div>
  )
}

export default CorrectAndRecognizedSolutionPage;
