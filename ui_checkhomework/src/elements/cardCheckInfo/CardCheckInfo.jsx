import { Button, Image, Progress, Typography } from "antd";
import { Link } from "react-router";

const conicColors = {
  '0%': '#ffccc7',
  '50%': '#ffe58f',
  '100%': '#87d068',
};

const CardCheckInfo = ({ style, taskImg }) => {
  return (
    <div style={{
      border:'1px solid #000',
      borderRadius:"20px",
      display:'flex',
      flexDirection:'column',
      justifyContent:'space-between',
      ...style
    }}>
      <div>
        <div style={{
          display:'flex',
          justifyContent:'space-between',
          alignItems:'center',
          padding:'0 20px',
          borderBottom:'1px solid #000'
        }}>
          <Typography.Title style={{
            width:'80%'
          }}>
            Иванов И. И.
          </Typography.Title>
          <div>Вар. 22</div>
        </div>

        <div style={{
          padding:'0 20px',
          borderBottom:'1px solid #000',
          display:'flex',
          justifyContent:'space-between',
          alignItems:'center',
        }}>
          <Link style={{
            padding:'10px 0',
            textDecoration:'none',
            color:'#000',
          }}>Назад</Link>
          <Link style={{
            padding:'10px 0',
            textDecoration:'none',
            color:'#000',
          }}>На главную</Link>
        </div>

        <div style={{
          padding:'0 20px',
          paddingBottom:'20px',
          borderBottom:'1px solid #000'
        }}>
          <Typography.Title level={5}>
            Задание №2
          </Typography.Title>
          <Image src={taskImg} style={{
            maxHeight:'30vh'
          }}> </Image>
        </div>
      </div>

      <div style={{
        padding:'10px 20px',
        flex:1,
        display:'flex',
        flexDirection:'column',
        alignItems:'center',
        justifyContent:'space-evenly'
      }}>
        <Button size="large" style={{
        padding:'30px 30px',
        border:'1px solid #000',
        borderRadius:"0"
      }}>Распознать</Button> 
        <div style={{
          padding:'10px 0'
        }}>
          <Progress size={150} type="circle" percent={0} strokeColor={conicColors} strokeWidth={10} status="normal" />
        </div>
      </div>

      <div style={{
        padding:'30px 20px',
        display:'flex',
        justifyContent:'space-between',
        alignItems:'center',
        borderTop:'1px solid #000'
      }}>
        <Button size="large" style={{
          padding:'30px 30px',
          border:'1px solid #000',
          borderRadius:"0"
        }}>Записать в БД</Button>
        <Button size="large" style={{
          padding:'30px 30px',
          border:'1px solid #000',
          borderRadius:"0"
        }}>Удалить</Button>
      </div>
    </div>
  )
}

export default CardCheckInfo;
