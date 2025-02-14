import Logo from '/logo.svg';
import Footer from '../../components/footer/Footer.jsx';

function Login(){
  return (
    <div className="flex flex-col items-center h-screen gap-5 p-8 bg-white-green">
      <div className='mt-10'>
        <img src={Logo} alt="logotipo" />
      </div>
      <form className="flex flex-col gap-5 w-full">
        <div>
          <input
            className="appearance-none border-none rounded w-full py-2 px-3 text-gray-700 bg-white focus:outline-none"
            id="email"
            type="email"
            placeholder="Email"
          />
        </div>
        <div>
          <input
            className="appearance-none border-none rounded w-full py-2 px-3 text-gray-700 mb-3 bg-white focus:outline-none"
            id="password"
            type="password"
            placeholder="Senha"
          />
        </div>
        <div>
          <button
            className="bg-greenpeace cursor-pointer text-white font-bold py-2 w-full rounded hover:bg-emerald"
            type="submit"
          >
            Entrar
          </button>
        </div>
      </form>
      <Footer title="Não tem uma conta? Cadastre-se" page="/cadastro" />
    </div>
  );
}

export default Login;