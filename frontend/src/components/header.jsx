import {Link} from 'react-router-dom'
import './header.css'
export default function Header(){
    return (
        <>
            <table>
                <tr>
                    <th className='header'>
                        <Link to={'/'}> Home!</Link>
                    </th>
                    <th className='header'>
                        <Link to={'/Calendar'}> Calendar!</Link>
                    </th>
                    <th className='header'>
                        <Link to={'/timer'}> MEATLOAF!!!</Link>
                    </th>

                </tr>
            </table>
        </>



    )



}