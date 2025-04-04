import "../styles/bootstrap.min.css";
import "../styles/style.css";
import "../styles/extra.css";
import React, { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import ThemeToggleButton from "../helper/ThemeToggleButton";

const MasterLayout = ({ children }) => {
  const [sidebarActive, setSidebarActive] = useState(true); // Sidebar initially open
  const location = useLocation();

  useEffect(() => {
    const handleDropdownClick = (event) => {
      event.preventDefault();
      const clickedDropdown = event.currentTarget.closest(".dropdown");
      if (!clickedDropdown) return;

      const isActive = clickedDropdown.classList.contains("open");
      document.querySelectorAll(".sidebar-menu .dropdown").forEach((dropdown) => {
        dropdown.classList.remove("open");
        const submenu = dropdown.querySelector(".sidebar-submenu");
        if (submenu) submenu.style.maxHeight = "0px";
      });

      if (!isActive) {
        clickedDropdown.classList.add("open");
        const submenu = clickedDropdown.querySelector(".sidebar-submenu");
        if (submenu) submenu.style.maxHeight = `${submenu.scrollHeight}px`;
      }
    };

    document.querySelectorAll(".sidebar-menu .dropdown-toggle").forEach((el) => {
      el.addEventListener("click", handleDropdownClick);
    });

    return () => {
      document.querySelectorAll(".sidebar-menu .dropdown-toggle").forEach((el) => {
        el.removeEventListener("click", handleDropdownClick);
      });
    };
  }, [location]);

  return (
    <div className={`page-wrapper ${sidebarActive ? 'sidebar-active' : ''}`}>
      {/* Sidebar */}
      <aside className="sidebar-wrapper">
        <div className="sidebar-brand">
          <Link to="/">Prizym.ai</Link>
        </div>
        <div className="sidebar-menu">
          <ul>
            <li className="dropdown">
              <NavLink to="/lens" className="dropdown-toggle">LENS (AI)</NavLink>
            </li>
            <li className="dropdown">
              <NavLink to="/spark" className="dropdown-toggle">SPARK (CRM)</NavLink>
            </li>
            <li className="dropdown">
              <NavLink to="/next" className="dropdown-toggle">NEXT (Marketplace)</NavLink>
            </li>
            <li className="dropdown">
              <NavLink to="/signin" className="dropdown-toggle">VITA (Sign In)</NavLink>
            </li>
            <li className="dropdown">
              <NavLink to="/signup" className="dropdown-toggle">VITA (Sign Up)</NavLink>
            </li>
          </ul>
        </div>
      </aside>

      {/* Main content */}
      <main className="main-content">
        <nav className="navbar">
          <button 
            className="btn btn-toggle-sidebar"
            onClick={() => setSidebarActive(!sidebarActive)}
          >
            ☰
          </button>
          <ThemeToggleButton />
        </nav>

        <section className="content-area">
          {children}
        </section>
      </main>
    </div>
  );
};

export default MasterLayout;
