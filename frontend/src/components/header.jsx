import {Link} from 'react-router-dom'
import './header.css'
export default function Header(){
    return (
        <>
            <table className='bar'>
                <tr>
                    <th className='header'>
                        <Link to={'/'}> Home!</Link>
                    </th>
                    <th className='header'>
                        <Link to={'/calendar/anteatery'}> Anteatery Calendar!</Link>
                    </th>
                    <th className='header'>
                        <Link to={'/calendar/brandywine'}> Brandywine Calendar!</Link>
                    </th>
                    <th className='header'>
                        <Link to={'/timer'}> MEATLOAF!!!</Link>
                    </th>

                </tr>
            </table>
        </>



    )



}