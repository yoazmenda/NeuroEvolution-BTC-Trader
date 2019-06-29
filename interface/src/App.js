import React from 'react';
import Chart from './components/chart';
import Parameters from './components/parameters';


class App extends React.Component {
  state = {
    activeHeader: 0
  }

  setActivePage(activePage) {
    this.setState({activeHeader: activePage})
  }

  getTabColor(idx) {
    return this.state.activeHeader === idx ? "rgb(20, 20, 20)" : "rgb(32,31,30)"
  }

  render() {
    const pageContent = [
      <Parameters />,
      <Chart />
    ]

    return (
      <div className="App">
        <div className="header">
          <span 
            className="header-item" 
            onClick={() => this.setActivePage(0)}
            style={{backgroundColor: this.getTabColor(0)}}
          >
              Training Parameters
          </span>
          <span 
            className="header-item" 
            onClick={() => this.setActivePage(1)}
            style={{backgroundColor: this.getTabColor(1)}}
          >
            Training Progress
          </span>
        </div>
        {pageContent[this.state.activeHeader]}
      </div>
    );
  }
}

export default App;
