import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/store/AuthContext';
import Header from '@/components/Header';
import Login from '@/pages/Login';
import Register from '@/pages/Register';
import Dashboard from '@/pages/Dashboard';
import TicketForm from '@/pages/TicketForm';
import TicketDetails from '@/pages/TicketDetails';
import TicketList from '@/pages/TicketList';
import UserProfile from '@/pages/UserProfile';
import NotificationCenter from '@/pages/NotificationCenter';
import OperatorDashboard from '@/pages/OperatorDashboard';
import MunicipalityManagement from '@/pages/MunicipalityManagement';
import AdminStats from '@/pages/AdminStats';

interface PrivateRouteProps {
  children: React.ReactNode;
  roles?: Array<'citizen' | 'operator' | 'admin'>;
}

function PrivateRoute({ children, roles }: PrivateRouteProps) {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Caricamento...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (roles && user && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" />;
  }

  return <>{children}</>;
}

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main>{children}</main>
    </div>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/profile"
        element={
          <PrivateRoute>
            <Layout>
              <UserProfile />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/notifications"
        element={
          <PrivateRoute>
            <Layout>
              <NotificationCenter />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/tickets"
        element={
          <PrivateRoute>
            <Layout>
              <TicketList />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/tickets/new"
        element={
          <PrivateRoute>
            <Layout>
              <TicketForm />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/tickets/:id"
        element={
          <PrivateRoute>
            <Layout>
              <TicketDetails />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/operator/dashboard"
        element={
          <PrivateRoute roles={['operator', 'admin']}>
            <Layout>
              <OperatorDashboard />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/municipality/management"
        element={
          <PrivateRoute roles={['admin']}>
            <Layout>
              <MunicipalityManagement />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/admin/stats"
        element={
          <PrivateRoute roles={['admin']}>
            <Layout>
              <AdminStats />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route path="/" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
