import { Image } from "antd";

const CardCheckInfo = ({ style, student = "Иванов И. И.", variant = "22", task = "2", img, recognizedImg }) => {
  return (
    <div
      style={{
        border: "1px solid #000",
        borderRadius: "20px",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "16px",
        backgroundColor: "#fff",
        ...style,
      }}
    >
      {/* ФИО + вариант */}
      <div
        style={{
          width: "100%",
          borderBottom: "1px solid #ccc",
          paddingBottom: "8px",
          marginBottom: "12px",
        }}
      >
        <h2 style={{ margin: 0, fontSize: "18px", fontWeight: "600" }}>{student}</h2>
        <div style={{ fontSize: "16px" }}>Вар. {variant}</div>
      </div>

      {/* Задание (основное фото) */}
      <div style={{ width: "100%" }}>
        <div style={{ marginBottom: "8px", fontWeight: "500" }}>Задание №{task}</div>
        {img ? (
          <Image
            src={img}
            alt="Решение"
            style={{
              width: "100%",
              maxHeight: "250px",
              objectFit: "contain",
              borderRadius: "8px",
              border: "1px solid #ccc",
            }}
          />
        ) : (
          <div
            style={{
              width: "100%",
              height: "200px",
              border: "1px dashed #aaa",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#777",
              borderRadius: "8px",
            }}
          >
            Фото решения отсутствует
          </div>
        )}
      </div>

      {/* Сравнение: эталон и распознанное */}
      <div style={{ display: "flex", gap: "12px", marginTop: "16px" }}>
        {/* Эталонная задача */}
        <div
          style={{
            flex: 1,
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "12px",
            textAlign: "center",
            background: "#fafafa",
          }}
        >
          <p style={{ fontWeight: "500", marginBottom: "8px" }}>Эталон</p>
          {img ? (
            <Image
              src={img}
              alt="Эталонная задача"
              style={{ maxHeight: "150px", objectFit: "contain" }}
            />
          ) : (
            <div style={{ fontSize: "14px", color: "#777" }}>Нет данных</div>
          )}
        </div>

        {/* Распознанная задача */}
        <div
          style={{
            flex: 1,
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "12px",
            textAlign: "center",
            background: "#fafafa",
          }}
        >
          <p style={{ fontWeight: "500", marginBottom: "8px" }}>Распознанное</p>
          {recognizedImg ? (
            <Image
              src={recognizedImg}
              alt="Распознанная задача"
              style={{ maxHeight: "150px", objectFit: "contain" }}
            />
          ) : (
            <div style={{ fontSize: "14px", color: "#777" }}>Нет данных</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CardCheckInfo;
