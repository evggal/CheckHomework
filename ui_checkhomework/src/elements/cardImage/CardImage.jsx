import { Image } from 'antd'

const CardImage = ({ style, img }) => {
  return (
    <div style={{
      width:"500px",
      height:"500px",
      border:'1px solid #000',
      borderRadius:"20px",
      overflow:"hidden",
      display:'flex',
      justifyContent:'center',
      alignItems:'center',
      ...style
    }}>
      <Image
      src={img}
      style={{
        objectFit:'contain'
      }}
      />
    </div>
  )
}

export default CardImage;
