  const htmlElement = document.documentElement;
  const themeSwitcher = document.getElementById('theme-switcher');
  const cyberpunkBtn = document.getElementById('theme-cyberpunk');

  // 1. Check local storage for a saved theme, or use system preference
  const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  // Set the site's theme on page load
  htmlElement.setAttribute('data-theme', savedTheme);
  
  // Keep the checkbox UI state matched up
  if (savedTheme === 'dark') {
    themeSwitcher.checked = true;
  }

  // 2. Toggle between Light and Dark
  themeSwitcher.addEventListener('change', (e) => {
    const newTheme = e.target.checked ? 'dark' : 'light';
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });

 


// Colors mapped from DaisyUI 'cyberpunk' theme (Yellow/Pink/Cyan base)
const options = {
    series: [{
        name: 'Workout Duration (Mins)',
        data: [30, 40, 35, 50, 45, 60, 55] // Static placeholder data
    }],
    chart: {
        type: 'area',
        height: 280,
        toolbar: { show: false }, // Hide ugly control buttons
        zoom: { enabled: false },
        fontFamily: 'inherit',
        background: 'transparent'
    },
    dataLabels: { enabled: false },
    stroke: {
        curve: 'smooth',
        width: 3,
        colors: ['#ff007f'] // Pink line to match cyberpunk accent
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.45,
            opacityTo: 0.05,
            stops: [0, 100],
            colorStops: [
                { offset: 0, color: '#ff007f', opacity: 0.4 },
                { offset: 100, color: '#ff007f', opacity: 0.0 }
            ]
        }
    },
    grid: {
        borderColor: '#ffed0033', // Slight yellow border opacity
        strokeDashArray: 4,
        yaxis: { lines: { show: true } }
    },
    xaxis: {
        categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        axisBorder: { show: false },
        axisTicks: { show: false },
        labels: {
            style: { colors: '#000', fontWeight: 600 }
        }
    },
    yaxis: {
        labels: {
            style: { colors: '#000', fontWeight: 600 }
        }
    },
    tooltip: {
        theme: 'dark',
        x: { show: true },
        marker: { show: false }
    }
};

const chart = new ApexCharts(document.querySelector("#workout-chart"), options);
chart.render();
