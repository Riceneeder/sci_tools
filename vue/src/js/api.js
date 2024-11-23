import axios from "axios";

// 检测当前是否为开发环境并设置 Axios 的基础 URL
if (import.meta.env.MODE === "development") {
  axios.defaults.baseURL = "http://127.0.0.1:5000";
  console.log(
    "Development mode, axios.defaults.baseURL : http://127.0.0.1:5000"
  );
}

/**
 * [GET] A class that provides static methods to interact with various API endpoints.
 */
class Get {
  /**
   * Fetches the list of APIs from the server.
   *
   * @returns {Promise} A promise that resolves to the response of the GET request to "/api".
   */
  static api_list() {
    return axios.get("/api");
  }

  /**
   * Fetches the public folder list from the server.
   *
   * @returns {Promise} A promise that resolves to the response of the GET request.
   */
  static public_list() {
    return axios.get("/api/get/public/list");
  }

  /**
   * Fetches the list of PDFs from the server.
   *
   * @returns {Promise} A promise that resolves to the response of the GET request.
   */
  static pdf_list() {
    return axios.get("/api/get/pdf/list");
  }

  /**
   * Fetches the list of markdown files.
   *
   * @returns {Promise} A promise that resolves to the response of the GET request to "/api/get/md/list".
   */
  static md_list() {
    return axios.get("/api/get/md/list");
  }

  /**
   * Downloads a public file from the server.
   *
   * @param {string} file_name - The name of the file to be downloaded.
   * @returns {Promise} - A promise that resolves to the response of the GET request.
   */
  static async download_public_file(file_name) {
    try {
      const response = await axios({
        url: "/api/download/public/" + file_name,
        method: "GET",
        responseType: "blob",
      })
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", file_name);
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
    }
  }
}

/**
 * [POST] A class that provides methods for interacting with various API endpoints.
 */
class Post {
  /**
   * Translates markdown content from one language to another.
   *
   * @param {string} source - The source language code.
   * @param {string} target - The target language code.
   * @returns {Promise} - A promise that resolves with the translation result.
   */
  static mdtranslate(source, target) {
    return axios.post("/api/mdtranslate/" + source + "/" + target);
  }

  /**
   * Uploads data to the server.
   *
   * @param {string} type - The type of data being uploaded.
   * @param {Object} data - The data to be uploaded.
   * @returns {Promise} - A promise that resolves to the server's response.
   */
  static upload(type, data) {
    return axios.post("/api/upload/" + type, data);
  }

  /**
   * Sends a POST request to the /api/sci_pdf2md endpoint.
   *
   * @returns {Promise} - The Axios promise for the HTTP request.
   */
  static sci_pdf2md() {
    return axios.post("/api/sci_pdf2md");
  }
}

/**
 * [DELETE] A class that provides static methods to delete different types of files from the server.
 */
class Delete {
  /**
   * Deletes a public file from the server.
   *
   * @param {string} file_name - The name of the file to be deleted.
   * @returns {Promise} - A promise that resolves to the response of the delete request.
   */
  static public_file(file_name) {
    return axios.delete("/api/delete/public/" + file_name);
  }

  /**
   * Deletes a PDF file from the server.
   *
   * @param {string} file_name - The name of the PDF file to be deleted.
   * @returns {Promise} - A promise that resolves to the response of the delete request.
   */
  static pdf_file(file_name) {
    return axios.delete("/api/delete/pdf/" + file_name);
  }

  /**
   * Deletes a markdown file on the server.
   *
   * @param {string} file_name - The name of the markdown file to delete.
   * @returns {Promise} - A promise that resolves to the response of the delete request.
   */
  static md_file(file_name) {
    return axios.delete("/api/delete/md/" + file_name);
  }
}

const API = { Get, Post, Delete };

export default API;
