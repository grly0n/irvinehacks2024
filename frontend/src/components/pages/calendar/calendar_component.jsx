
import "./calendar_component.css"

/* pipe in the data here*/



function Calendar({data}) {
  const date= new Date();
  const current_month=date.getMonth();
  const current_day=date.getDate();
  const current_year=date.getFullYear();
  let food={};
  let dates= Object.keys(data);
  


  const createTable =()=>{
    let table = []
    
      let children = []
      for (let j=0;j<7;j++)
      {
        let input=[];
        
        let todays_food=data[dates[j]]
        
        let lunch= todays_food['Lunch'];
        input.push(dates[j]);
        input.push(<h2>Lunch</h2>);
        console.log(input);

        let lunch_areas=Object.keys(lunch);
        for (const areas of lunch_areas)
        {
          let string_list=areas;

          for (const foods of lunch[areas] ){
            string_list= string_list+ '\n'+foods;
          }
          input.push(<pre>{string_list}</pre>);
        }
        
        
        
        let dinner= todays_food['Dinner'];

        input.push(<h2>Dinner</h2>);
        console.log(input);

        let dinner_areas=Object.keys(dinner);
        for (const areas of dinner_areas)
        {
          let string_list=areas;

          for (const foods of dinner[areas] ){
            string_list= string_list+ '\n'+foods;
          }
          input.push(<pre>{string_list}</pre>);
        }
        children.push(<th className="food">{input}</th>);
        

      }
      table.push(<tr>{children}</tr>)
      
      children = []
      for (let j=7;j<14;j++)
      {
        let input=[];
        let todays_food=data[dates[j]]
        let lunch= todays_food['Lunch'];
        input.push(dates[j]);
        input.push(<h2>Lunch</h2>);
        

        let lunch_areas=Object.keys(lunch);
        for (const areas of lunch_areas)
        {
          let string_list=areas;

          for (const foods of lunch[areas] ){
            string_list= string_list+ '\n'+foods;
          }
          input.push(<pre>{string_list}</pre>);
        }
        let dinner= todays_food['Dinner'];
        input.push(<h2>Dinner</h2>);

        let dinner_areas=Object.keys(dinner);
        for (const areas of dinner_areas)
        {
          let string_list=areas;

          for (const foods of dinner[areas] ){
            string_list= string_list+ '\n'+foods;
          }
          input.push(<pre>{string_list}</pre>);
        }

        children.push(<th className="food">{input}</th>);
        

      }
      table.push(<tr>{children}</tr>)


    
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
