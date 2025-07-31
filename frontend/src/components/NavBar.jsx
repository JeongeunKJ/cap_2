import { Link } from 'react-router-dom';

function NavBar() {
    return (
        <div className="fixed top-4 right-4 flex flex-col gap-2">
            <Link to="/" className="bg-blue-500 text-white px-4 py-2 rounded shadow">홈</Link>
            <Link to="/analysis" className="bg-green-500 text-white px-4 py-2 rounded shadow">분석</Link>
            <Link to="/join" className="bg-purple-500 text-white px-4 py-2 rounded shadow">결합</Link>
        </div>
    );
}

export default NavBar;