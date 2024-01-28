
import "./calendar_component.css"

/* pipe in the data here*/



function Calendar({data}) {
  const date= new Date();
  const current_month=date.getMonth();
  const current_day=date.getDate();
  const current_year=date.getFullYear();
  let food={};
  let dates= Object.keys(data)
  
  {for (let i =0;i<data.length;i++)
  {
    if (current_month==8 | current_month==3 | current_month==5|current_month==10){
      if (current_day+i>30) {
        food[(current_month+2)+'/'+((current_day+i)%30) +'/'+current_year]= data[i];
      }
      else{
        food[(current_month+1)+'/'+(current_day+i) +'/'+current_year]= data[i];
      }
    }
    else if (current_month==1){
      if (current_day+i>28) {
        food[(current_month+2)+'/'+((current_day+i)%28) +'/'+current_year]= data[i];
      }
      else{
        food[(current_month+1)+'/'+(current_day+i) +'/'+current_year]= data[i];
      }
    }
    else{
      if (current_day+i>31) {
        food[(current_month+2)+'/'+((current_day+i)%31) +'/'+current_year]= data[i];
      }
      else{
        food[(current_month+1)+'/'+(current_day+i) +'/'+current_year]= data[i];
      }

    }
  }}
  
  let keys= Object.keys(food);


  const createTable =()=>{
    let table = []
    for ( let i =0; i<2;i++)
    {
      let children = []
      for (let j=0;j<keys.length;j++)
      {
        children.push(<td>{keys[j]+'-'+food[keys[j]]}</td>)


      }
      table.push(<tr>{children}</tr>)


    }
    return table
  } 

  return (
    <>
      
      <table  className='Calend'>
        <tr>
          <th className='days'>Sunday</th>
          <th className='days'>Monday</th>
          <th className='days'>Tuesday</th>
          <th className='days'>Wednesday</th>
          <th className='days'>Thursday</th>
          <th className='days'>Friday</th>
          <th className='days'>Saturday</th>
          


        </tr>
        {createTable()}
      </table>
    </>
    
  );
}


export default Calendar;
