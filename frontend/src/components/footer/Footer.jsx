import { useNavigate } from "react-router";

function Footer({ title, page }) {
  let navigate = useNavigate();

  return (
    <footer className="fixed bottom-0 w-full bg-primary text-center p-4 border-t-2 border-emerald">
      <button
        className="text-white underline text-lg cursor-pointer"
        onClick={() => navigate(`${page}`)}
      >
        {title}
      </button>
    </footer>
  );
}

export default Footer;
