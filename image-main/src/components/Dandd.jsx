// import { useState, useRef } from "react";

// const Dandd = () => {
//   const [image, setImage] = useState(null);
//   const inputRef = useRef();

//   const handleDragOver = (event) => {
//     event.preventDefault();
//   };

//   const handleDrop = (event) => {
//     event.preventDefault();
//     setImage(event.dataTransfer.files);
//   };

//   // send files to the server
//   async function uploadImage() {
//     console.log("uploaded");
//     console.log(image);
//     const formData = new FormData();
//     formData.append("image", image[0]);

//     const response = await fetch("http://127.0.0.1:8000/api/products/", {
//       method: "POST",
//       body: formData,
//     })
//       .then((response) => response.json())
//       .catch((error) => console.log(error));
//   }

//   if (image) {
//     return (
//       <div className="flex flex-col justify-center items-center rounded-2xl absolute top-[50%] left-[50%]  translate-x-[-50%] translate-y-[-50%]  w-80 shadow-2xl h-60">
//         <ul>
//           {Array.from(image).map((image, idx) => (
//             <li key={idx}>{image.name}</li>
//           ))}
//         </ul>
//         <div className="mt-4">
//           <button
//             onClick={() => setImage(null)}
//             className="bg-blue-500 mr-5 py-2 px-4 rounded-xl"
//           >
//             Cancel
//           </button>
//           <button
//             onClick={uploadImage}
//             className="bg-blue-500 px-4 py-2 rounded-xl "
//           >
//             Upload
//           </button>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div
//       className="flex flex-col justify-center items-center rounded-2xl absolute top-[50%] left-[50%]  translate-x-[-50%] translate-y-[-50%]  w-80 shadow-2xl h-60"
//       onDragOver={handleDragOver}
//       onDrop={handleDrop}
//     >
//       <p>Drag and Drop Files to Upload</p>
//       <p>Or</p>
//       <input
//         type="file"
//         multiple
//         onChange={(event) => setImage(event.target.files)}
//         hidden
//         accept="image/png, image/jpeg"
//         ref={inputRef}
//       />
//       <button
//         onClick={() => inputRef.current.click()}
//         className="bg-blue-800 text-white font-bold rounded-full px-4 py-2"
//       >
//         Select Files
//       </button>
//     </div>
//   );
// };

// export default Dandd;



// ***change by ishan***
import { useState, useRef } from "react";

const Dandd = () => {
  const [image, setImage] = useState(null);
  const [colorizedImageUrl, setColorizedImageUrl] = useState(null);
  const inputRef = useRef();

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setImage(event.dataTransfer.files);
  };

  async function uploadImage() {
    const formData = new FormData();
    formData.append("image", image[0]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/products/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.colorized_image_url) {
        setColorizedImageUrl(data.colorized_image_url);
      } else {
        console.error("Server response is missing colorized_image_url:", data);
      }
    } catch (error) {
      console.error("Error uploading image:", error);
    }
  }

  if (colorizedImageUrl) {
    return (
      <div className="flex flex-col justify-center items-center">
        <img src={colorizedImageUrl} alt="Colorized Image" onError={() => console.error("Error loading image")} />
      </div>
    );
  }

  if (image) {
    return (
      <div className="flex flex-col justify-center items-center rounded-2xl absolute top-[50%] left-[50%]  translate-x-[-50%] translate-y-[-50%]  w-80 shadow-2xl h-60">
        <ul>
          {Array.from(image).map((image, idx) => (
            <li key={idx}>{image.name}</li>
          ))}
        </ul>
        <div className="mt-4">
          <button
            onClick={() => setImage(null)}
            className="bg-blue-500 mr-5 py-2 px-4 rounded-xl"
          >
            Cancel
          </button>
          <button
            onClick={uploadImage}
            className="bg-blue-500 px-4 py-2 rounded-xl "
          >
            Upload
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className="flex flex-col justify-center items-center rounded-2xl absolute top-[50%] left-[50%]  translate-x-[-50%] translate-y-[-50%]  w-80 shadow-2xl h-60"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <p>Drag and Drop Files to Upload</p>
      <p>Or</p>
      <input
        type="file"
        multiple
        onChange={(event) => setImage(event.target.files)}
        hidden
        accept="image/png, image/jpeg"
        ref={inputRef}
      />
      <button
        onClick={() => inputRef.current.click()}
        className="bg-blue-800 text-white font-bold rounded-full px-4 py-2"
      >
        Select Files
      </button>
    </div>
  );
};

export default Dandd;


//change to be made by anup:
// "http://127.0.0.1:8000/api/products/" yo api image upload garna ko lagi ho database ma
// "http://127.0.0.1:8000/api/colorized-image/ yo api image retrieve garna ko lagi ho . Yo mathi ko code ma tyo milayeko chaina tyo milauna paryo hai.