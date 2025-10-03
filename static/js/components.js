// React Components for Inventory Management System

// DataCard Component
const DataCard = ({ title, value, icon, color }) => {
    return (
        <div className="col-md-3 mb-4">
            <div className="card h-100">
                <div className="card-body d-flex align-items-center">
                    <div className={`icon-box bg-${color} text-white`}>
                        <i className={`fas ${icon}`}></i>
                    </div>
                    <div className="ms-3">
                        <h6 className="card-subtitle text-muted">{title}</h6>
                        <h2 className="card-title mb-0">{value}</h2>
                    </div>
                </div>
            </div>
        </div>
    );
};

// SearchBar Component
const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = React.useState('');
    
    const handleSearch = (e) => {
        e.preventDefault();
        onSearch(query);
    };
    
    return (
        <form className="search-form mb-4" onSubmit={handleSearch}>
            <div className="input-group">
                <input 
                    type="text" 
                    className="form-control" 
                    placeholder="Search..." 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button className="btn btn-primary" type="submit">
                    <i className="fas fa-search"></i>
                </button>
            </div>
        </form>
    );
};

// ProductTable Component
class ProductTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            products: [],
            loading: true,
            error: null
        };
    }
    
    componentDidMount() {
        // In a real React app, we would fetch data from an API
        // For now, we'll just use the data passed from the template
        const productsData = document.getElementById('products-data');
        if (productsData) {
            try {
                const products = JSON.parse(productsData.textContent);
                this.setState({ products, loading: false });
            } catch (error) {
                this.setState({ error: 'Failed to load products', loading: false });
            }
        }
    }
    
    render() {
        const { products, loading, error } = this.state;
        
        if (loading) return <div className="text-center py-4"><i className="fas fa-spinner fa-spin"></i> Loading...</div>;
        if (error) return <div className="alert alert-danger">{error}</div>;
        
        return (
            <div className="card">
                <div className="card-header d-flex justify-content-between align-items-center">
                    <h5 className="mb-0">Products</h5>
                    <a href="/add_product" className="btn btn-sm btn-primary">
                        <i className="fas fa-plus"></i> Add New
                    </a>
                </div>
                <div className="card-body">
                    <div className="table-responsive">
                        <table className="table table-hover">
                            <thead>
                                <tr>
                                    <th>Product ID</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {products.length > 0 ? (
                                    products.map(product => (
                                        <tr key={product.product_id}>
                                            <td>{product.product_id}</td>
                                            <td>
                                                <a href={`/edit_product/${product.product_id}`} className="btn btn-sm btn-warning me-2">
                                                    <i className="fas fa-edit"></i>
                                                </a>
                                                <button className="btn btn-sm btn-danger" 
                                                        onClick={() => confirm('Are you sure you want to delete this product?')}>
                                                    <i className="fas fa-trash"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="2" className="text-center">No products found</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        );
    }
}

// Render React components if their containers exist
document.addEventListener('DOMContentLoaded', function() {
    const productTableContainer = document.getElementById('react-product-table');
    if (productTableContainer) {
        ReactDOM.render(<ProductTable />, productTableContainer);
    }
    
    // Add more component renders as needed
});