
import "./App.css"

/* pipe in the data here*/
const data=["meatloaf","taco", "breadstick", "meatloaf","meatloaf","meatloaf","meatloaf"]


function Calender() {
  const date= new Date();
  const current_month=date.getMonth();
  const current_day=date.getDate();
  const current_year=date.getFullYear()

  let mon= data[0]
  let tues = data[1]
  let wed = data[2]
  let thurs = data[3]
  let fri = data[4]
  let sat = data[5]
  let sun = data[6]
  return (
    <>
      
      <table  className='Calend'>
        <tr>
          <th className='days'>Monday</th>
          <th className='days'>Tuesday</th>
          <th className='days'>Wednesday</th>
          <th className='days'>Thursday</th>
          <th className='days'>Friday</th>
          <th className='days'>Saturday</th>
          <th className='days'>Sunday</th>


        </tr>
        
        <tr>
          <th className='food'>{mon} </th>
          <th className='food'>{tues} </th>
          <th className='food'>{wed} </th>
          <th className='food'>{thurs} </th>
          <th className='food'>{fri} </th>
          <th className='food'>{sat} </th>
          <th className='food'>{sun} </th>

        </tr>




      </table>
      

      
    
    </>
    
  );
}



export default Calender
