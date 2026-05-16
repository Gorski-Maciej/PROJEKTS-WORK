import { Link, Route, Routes } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Incidents from './pages/Incidents'
import Recommendations from './pages/Recommendations'
import './styles/app.css'

export default function App(){
  return <main><h2>NetAegis</h2><nav><Link to='/'>Dashboard</Link><Link to='/incidents'>Incidents</Link><Link to='/recommendations'>Recommendations</Link></nav><Routes><Route path='/' element={<Dashboard/>}/><Route path='/incidents' element={<Incidents/>}/><Route path='/recommendations' element={<Recommendations/>}/></Routes></main>
}
