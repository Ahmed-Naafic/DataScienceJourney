import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Car,
    BarChart3,
    TrendingUp,
    History,
    Settings,
    DollarSign,
    Activity,
    Layers,
    Fuel,
    Cpu,
    Download
} from 'lucide-react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement
);

const API_BASE = '/api';

function App() {
    const [metadata, setMetadata] = useState<any>(null);
    const [stats, setStats] = useState<any>(null);
    const [sampleData, setSampleData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [prediction, setPrediction] = useState<number | null>(null);
    const [form, setForm] = useState({
        Brand: '',
        Year: 2020,
        Engine_Size: 2.0,
        Fuel_Type: '',
        Transmission: '',
        Mileage: 50000,
        Condition: '',
        Model: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [metaRes, statsRes, sampleRes] = await Promise.all([
                    axios.get(`${API_BASE}/eda/metadata`),
                    axios.get(`${API_BASE}/eda/stats`),
                    axios.get(`${API_BASE}/eda/sample`)
                ]);
                setMetadata(metaRes.data);
                setStats(statsRes.data);
                setSampleData(sampleRes.data);

                // Initial form values
                setForm(prev => ({
                    ...prev,
                    Brand: metaRes.data.brands[0],
                    Fuel_Type: metaRes.data.fuel_types[0],
                    Transmission: metaRes.data.transmissions[0],
                    Condition: metaRes.data.conditions[0],
                    Model: metaRes.data.models[0]
                }));
            } catch (err) {
                console.error("Error fetching data", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const handlePredict = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await axios.post(`${API_BASE}/predict`, form);
            setPrediction(res.data.predicted_price);
        } catch (err) {
            console.error("Prediction error", err);
            alert("Failed to get prediction. Check if the model is loaded.");
        }
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'white' }}>
                <div className="animate-pulse">Loading Antigravity AI Dashboard...</div>
            </div>
        );
    }

    const brandChartData = {
        labels: stats ? Object.keys(stats.brand_counts) : [],
        datasets: [{
            label: 'Cars by Brand',
            data: stats ? Object.values(stats.brand_counts) : [],
            backgroundColor: 'rgba(99, 102, 241, 0.6)',
            borderColor: 'rgba(99, 102, 241, 1)',
            borderWidth: 1,
        }]
    };

    const fuelChartData = {
        labels: stats ? Object.keys(stats.fuel_type_counts) : [],
        datasets: [{
            label: 'Fuel Type Distribution',
            data: stats ? Object.values(stats.fuel_type_counts) : [],
            backgroundColor: [
                'rgba(99, 102, 241, 0.6)',
                'rgba(34, 197, 94, 0.6)',
                'rgba(245, 158, 11, 0.6)',
                'rgba(239, 68, 68, 0.6)',
                'rgba(168, 85, 247, 0.6)',
            ],
            borderWidth: 1,
        }]
    };

    const handleDownload = () => {
        window.open(`${API_BASE}/download-report`, '_blank');
    };

    return (
        <div className="app-container">
            <nav className="navbar">
                <div className="logo d-flex align-items-center gap-2">
                    <Car size={32} />
                    <span>CarPredict</span>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="btn btn-primary" style={{ padding: '0.5rem 1rem' }} onClick={handleDownload}>
                        <Download size={18} />
                        Download Report
                    </button>
                </div>
            </nav>

            <main className="main-content">
                <header style={{ marginBottom: '2rem' }}>
                    <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Dashboard Overview</h1>
                    <p style={{ color: 'var(--text-muted)' }}>Real-time analytics and predictive modeling for car valuation.</p>
                </header>

                {/* Stats Cards */}
                <div className="grid">
                    <div className="card animate-fade-in" style={{ animationDelay: '0.1s' }}>
                        <div className="card-title"><Activity size={20} /> Total Dataset Volume</div>
                        <div className="stat-value">{stats?.total_rows.toLocaleString()}</div>
                        <div className="stat-label">Car records analyzed</div>
                    </div>
                    <div className="card animate-fade-in" style={{ animationDelay: '0.2s' }}>
                        <div className="card-title"><TrendingUp size={20} /> Model Accuracy</div>
                        <div className="stat-value">{Math.round((metadata?.r2 || 0) * 100)}%</div>
                        <div className="stat-label">R-squared Score (Validation)</div>
                    </div>
                    <div className="card animate-fade-in" style={{ animationDelay: '0.3s' }}>
                        <div className="card-title"><DollarSign size={20} /> Average Price</div>
                        <div className="stat-value">${Math.round((Object.values(stats?.avg_price_by_brand || {}) as number[]).reduce((a, b) => a + b, 0) / (Object.keys(stats?.avg_price_by_brand || {}).length || 1)).toLocaleString()}</div>
                        <div className="stat-label">Across all brands</div>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem', marginBottom: '2rem' }}>
                    {/* Prediction Form */}
                    <div className="card animate-fade-in" style={{ animationDelay: '0.4s' }}>
                        <div className="card-title"><Cpu size={20} /> AI Price Predictor</div>
                        <form onSubmit={handlePredict}>
                            <div className="form-group">
                                <label className="form-label">Brand</label>
                                <select className="form-control" value={form.Brand} onChange={e => setForm({ ...form, Brand: e.target.value })}>
                                    {metadata?.brands.map((b: string) => <option key={b} value={b}>{b}</option>)}
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Model</label>
                                <select className="form-control" value={form.Model} onChange={e => setForm({ ...form, Model: e.target.value })}>
                                    {metadata?.models.map((m: string) => <option key={m} value={m}>{m}</option>)}
                                </select>
                            </div>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <div className="form-group">
                                    <label className="form-label">Year</label>
                                    <input type="number" className="form-control" value={form.Year} onChange={e => setForm({ ...form, Year: parseInt(e.target.value) })} />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Engine Size (L)</label>
                                    <input type="number" step="0.1" className="form-control" value={form.Engine_Size} onChange={e => setForm({ ...form, Engine_Size: parseFloat(e.target.value) })} />
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Fuel Type</label>
                                <select className="form-control" value={form.Fuel_Type} onChange={e => setForm({ ...form, Fuel_Type: e.target.value })}>
                                    {metadata?.fuel_types.map((f: string) => <option key={f} value={f}>{f}</option>)}
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Transmission</label>
                                <select className="form-control" value={form.Transmission} onChange={e => setForm({ ...form, Transmission: e.target.value })}>
                                    {metadata?.transmissions.map((t: string) => <option key={t} value={t}>{t}</option>)}
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Mileage</label>
                                <input type="number" className="form-control" value={form.Mileage} onChange={e => setForm({ ...form, Mileage: parseInt(e.target.value) })} />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Condition</label>
                                <select className="form-control" value={form.Condition} onChange={e => setForm({ ...form, Condition: e.target.value })}>
                                    {metadata?.conditions.map((c: string) => <option key={c} value={c}>{c}</option>)}
                                </select>
                            </div>
                            <button type="submit" className="btn btn-primary btn-block">Predict Price</button>
                        </form>

                        {prediction !== null && (
                            <div className="prediction-result animate-fade-in">
                                <div className="stat-label">Estimated Market Value</div>
                                <div className="prediction-price">${prediction.toLocaleString()}</div>
                            </div>
                        )}
                    </div>

                    {/* Charts */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div className="card animate-fade-in" style={{ flex: 1, animationDelay: '0.5s' }}>
                            <div className="card-title"><BarChart3 size={20} /> Inventory by Brand</div>
                            <div style={{ height: '250px' }}>
                                <Bar
                                    data={brandChartData}
                                    options={{
                                        maintainAspectRatio: false,
                                        plugins: { legend: { display: false } },
                                        scales: { y: { grid: { color: 'rgba(255,255,255,0.1)' } } }
                                    }}
                                />
                            </div>
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', flex: 1 }}>
                            <div className="card animate-fade-in" style={{ animationDelay: '0.6s' }}>
                                <div className="card-title"><Fuel size={20} /> Fuel Types</div>
                                <div style={{ height: '200px' }}>
                                    <Pie data={fuelChartData} options={{ maintainAspectRatio: false }} />
                                </div>
                            </div>
                            <div className="card animate-fade-in" style={{ animationDelay: '0.7s' }}>
                                <div className="card-title"><Layers size={20} /> Top Models</div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                    {stats && Object.entries(stats.top_models).slice(0, 5).map(([model, count]: any) => (
                                        <div key={model} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <span style={{ fontSize: '0.875rem' }}>{model}</span>
                                            <span className="badge" style={{ background: 'var(--primary)', padding: '2px 8px', borderRadius: '10px', fontSize: '0.75rem' }}>{count}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Data Table Snippet */}
                <div className="card animate-fade-in" style={{ animationDelay: '0.8s' }}>
                    <div className="card-title"><History size={20} /> Dataset Sample (Top 10)</div>
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Brand</th>
                                    <th>Model</th>
                                    <th>Year</th>
                                    <th>Engine</th>
                                    <th>Fuel</th>
                                    <th>Mileage</th>
                                    <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {sampleData.map((row: any, i: number) => (
                                    <tr key={i}>
                                        <td>{row.Brand}</td>
                                        <td>{row.Model}</td>
                                        <td>{row.Year}</td>
                                        <td>{row['Engine Size']}L</td>
                                        <td>{row['Fuel Type']}</td>
                                        <td>{row.Mileage.toLocaleString()}</td>
                                        <td style={{ fontWeight: 600, color: 'var(--success)' }}>${row.Price.toLocaleString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
