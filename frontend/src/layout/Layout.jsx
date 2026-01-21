import { Outlet } from "react-router-dom";
import Nav from "../components/Navbar";
import Footer from "../components/Footer";

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col bg-linear-to-br from-purple-50 to-pink-50">
      <Nav />

      {/* CONTENIDO PRINCIPAL */}
      <main className="flex-1">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
};

export default Layout;
