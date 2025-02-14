import { useNavigate } from "react-router";

function Footer({ title, page, backgroundColor }) {
  let navigate = useNavigate();

  return (
    <footer
      className={`fixed bottom-0 w-full text-center p-4 border-t-2 border-emerald bg-${backgroundColor}`}
    >
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
