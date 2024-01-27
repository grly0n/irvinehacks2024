

function Calender() {
  const date= new Date();
  const current_month=date.getMonth();
  const current_day=date.getDate();
  const current_year=date.getFullYear()

  
  return (
    <>
      
      <table className='Calends'>
        <tr>
          <th>Monday</th>
          <th>Tuesday</th>
          <th>Wednesday</th>
          <th>Thursday</th>
          <th>Friday</th>
          <th>Saturday</th>
          <th>Sunday</th>


        </tr>




      </table>
      

      
    
    </>
    
  );
}



export default Calender
