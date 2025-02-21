import axios from "axios";

const api = axios.create({
  baseURL: "https://grant-89eg.onrender.com/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

const apiRequest = async (
  method,
  url,
  data = {},
  headers = {},
  successCallback,
  errorCallback,
  setloading
) => {
  const source = axios.CancelToken.source();
  const timeout = setTimeout(() => {
    source.cancel("Request timed out");
    alert("The request is taking too long. Please try again later.");
  }, 300000);

  try {
    const isFormData = data instanceof FormData; // Check if data is FormData

    const response = await api({
      method,
      url,
      data,
      headers: {
        ...headers,
        ...(headers.token ? { Authorization: `Bearer ${headers.token}` } : {}),
        ...(isFormData ? { "Content-Type": "multipart/form-data" } : {}),
      },
      cancelToken: source.token,
    });

    clearTimeout(timeout);

    if (successCallback) {
      successCallback(response.data);
    }
  } catch (error) {
    clearTimeout(timeout);
    if (axios.isCancel(error)) {
      console.log("Request canceled", error.message);
    } else {
      if (errorCallback) {
        errorCallback(error.response ? error.response.data : error.message);
      }
    }
  } finally {
    if (setloading) {
      setloading(false);
    }
  }
};

export const get = (
  url,
  headers,
  successCallback,
  errorCallback,
  setloading
) => {
  return apiRequest(
    "get",
    url,
    undefined, // No data for GET request
    headers,
    successCallback,
    errorCallback,
    setloading
  );
};

export const post = (
  url,
  data,
  headers,
  successCallback,
  errorCallback,
  setloading
) => {
  return apiRequest(
    "post",
    url,
    data,
    headers,
    successCallback,
    errorCallback,
    setloading
  );
};

export const put = (
  url,
  data,
  headers,
  successCallback,
  errorCallback,
  setloading
) => {
  return apiRequest(
    "put",
    url,
    data,
    headers,
    successCallback,
    errorCallback,
    setloading
  );
};

export const del = (
  url,
  headers,
  successCallback,
  errorCallback,
  setloading
) => {
  return apiRequest(
    "delete",
    url,
    undefined, // No data for DELETE request
    headers,
    successCallback,
    errorCallback,
    setloading
  );
};

export default api;
