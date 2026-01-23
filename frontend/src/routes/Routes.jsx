import { createBrowserRouter } from "react-router-dom";
import Layout from "../layout/Layout";
import Home from "../pages/Home";
import LoadingScreen from "../pages/LoadingScreen";


export const router = createBrowserRouter([
  // ⬇️ Página de carga al entrar en /
  {
    path: "/",
    element: <LoadingScreen />,
  },

  // ⬇️ App real bajo /app
  {
    path: "/app",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      }
    ]
  },

], {
  basename: "/content_generator"
});
