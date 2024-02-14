import Nav from "../components/Navb";
import Dandd from "../components/Dandd";
import { useEffect, useState } from "react";

function Home() {
  const user = localStorage.getItem("token");
  return (
    <div className="flex flex-col gap-10 ">
      {user == null ? <h1>Login to Colorize Image</h1> : <Dandd />}
    </div>
  );
}

export default Home;
