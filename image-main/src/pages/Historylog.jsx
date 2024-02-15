const Historylog = () => {
  const token = localStorage.getItem("token");
  decoded_token = jwt.decode(token, "secret", (algorithms = ["HS256"]));
  user_id = decoded_token["id"];
  return <p>history</p>;
};

export default Historylog;
