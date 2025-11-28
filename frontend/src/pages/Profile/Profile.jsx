import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { User, Mail, Phone, Calendar, Tag, CreditCard, Clock, CheckCircle, XCircle } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";
import { subscriptionService } from "../../services/api";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const { user, isAuthenticated, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    const fetchSubscription = async () => {
      try {
        if (user?.id) {
          const response = await subscriptionService.getSubscriptionStatus(user.id);
          if (response.data.success) {
            setSubscription(response.data.subscription);
          }
        }
      } catch (err) {
        console.error("Failed to fetch subscription:", err);
        setError("Failed to load subscription information");
      } finally {
        setLoading(false);
      }
    };

    fetchSubscription();
    // Refresh user data to get latest subscription tier
    if (refreshUser) {
      refreshUser();
    }
  }, [user, isAuthenticated, navigate, refreshUser]);

  const getTierColor = (tier) => {
    switch (tier?.toLowerCase()) {
      case "pro":
        return "from-cyan-500 to-blue-500";
      case "enterprise":
        return "from-purple-500 to-indigo-500";
      default:
        return "from-gray-500 to-gray-600";
    }
  };

  const getTierBadgeColor = (tier) => {
    switch (tier?.toLowerCase()) {
      case "pro":
        return "bg-cyan-500/20 text-cyan-300 border-cyan-500/50";
      case "enterprise":
        return "bg-purple-500/20 text-purple-300 border-purple-500/50";
      default:
        return "bg-gray-500/20 text-gray-300 border-gray-500/50";
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    } catch {
      return "Invalid date";
    }
  };

  const getDaysUntilRenewal = (dateString) => {
    if (!dateString) return null;
    try {
      const renewalDate = new Date(dateString);
      const today = new Date();
      const diffTime = renewalDate - today;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays;
    } catch {
      return null;
    }
  };

  const currentTier = subscription?.plan_name || "Free";
  const renewalDate = subscription?.next_billing_at 
    ? new Date(subscription.next_billing_at * 1000).toISOString()
    : null;
  const daysUntilRenewal = renewalDate ? getDaysUntilRenewal(renewalDate) : null;
  const isActive = subscription?.status === "active";

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-2">Profile</h1>
          <p className="text-gray-400">Manage your account and subscription</p>
        </motion.div>

        {/* Subscription Status Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className={`mb-6 rounded-2xl border p-6 bg-gradient-to-br ${getTierColor(currentTier)}/10 border-white/10 backdrop-blur-sm`}
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">Subscription</h2>
              <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-semibold border ${getTierBadgeColor(currentTier)}`}>
                {isActive ? (
                  <CheckCircle className="w-4 h-4" />
                ) : (
                  <XCircle className="w-4 h-4" />
                )}
                {currentTier} {isActive ? "Active" : "Inactive"}
              </span>
            </div>
            {currentTier !== "Free" && (
              <button
                onClick={() => navigate("/subscription")}
                className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-sm font-medium transition-colors"
              >
                Manage Subscription
              </button>
            )}
          </div>

          {currentTier !== "Free" && renewalDate && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div className="bg-black/30 rounded-lg p-4">
                <div className="flex items-center gap-2 text-gray-400 mb-2">
                  <Clock className="w-4 h-4" />
                  <span className="text-xs uppercase tracking-wider">Next Renewal</span>
                </div>
                <p className="text-white font-semibold">{formatDate(renewalDate)}</p>
                {daysUntilRenewal !== null && (
                  <p className="text-sm text-gray-400 mt-1">
                    {daysUntilRenewal > 0 
                      ? `${daysUntilRenewal} day${daysUntilRenewal !== 1 ? 's' : ''} remaining`
                      : daysUntilRenewal === 0
                      ? "Renews today"
                      : "Expired"}
                  </p>
                )}
              </div>
              <div className="bg-black/30 rounded-lg p-4">
                <div className="flex items-center gap-2 text-gray-400 mb-2">
                  <CreditCard className="w-4 h-4" />
                  <span className="text-xs uppercase tracking-wider">Status</span>
                </div>
                <p className="text-white font-semibold capitalize">{subscription?.status || "Unknown"}</p>
                {subscription?.razorpay_subscription_id && (
                  <p className="text-xs text-gray-400 mt-1">
                    ID: {subscription.razorpay_subscription_id.slice(0, 12)}...
                  </p>
                )}
              </div>
            </div>
          )}

          {currentTier === "Free" && (
            <div className="mt-4 p-4 bg-black/30 rounded-lg">
              <p className="text-gray-300 text-sm">
                Upgrade to Pro or Enterprise to unlock premium features and unlimited verifications.
              </p>
              <button
                onClick={() => navigate("/subscription")}
                className="mt-3 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg text-sm font-semibold hover:from-cyan-600 hover:to-blue-600 transition-all"
              >
                View Plans
              </button>
            </div>
          )}
        </motion.div>

        {/* User Information Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm mb-6"
        >
          <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
            <User className="w-5 h-5" />
            Personal Information
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs uppercase tracking-wider text-gray-400 mb-2">
                Full Name
              </label>
              <div className="flex items-center gap-3 p-3 bg-black/30 rounded-lg">
                <User className="w-4 h-4 text-gray-400" />
                <span className="text-white">{user?.name || "Not provided"}</span>
              </div>
            </div>

            <div>
              <label className="block text-xs uppercase tracking-wider text-gray-400 mb-2">
                Email
              </label>
              <div className="flex items-center gap-3 p-3 bg-black/30 rounded-lg">
                <Mail className="w-4 h-4 text-gray-400" />
                <span className="text-white">{user?.email || "Not provided"}</span>
              </div>
            </div>

            <div>
              <label className="block text-xs uppercase tracking-wider text-gray-400 mb-2">
                Phone Number
              </label>
              <div className="flex items-center gap-3 p-3 bg-black/30 rounded-lg">
                <Phone className="w-4 h-4 text-gray-400" />
                <span className="text-white">{user?.phone_number || "Not provided"}</span>
              </div>
            </div>

            <div>
              <label className="block text-xs uppercase tracking-wider text-gray-400 mb-2">
                Age
              </label>
              <div className="flex items-center gap-3 p-3 bg-black/30 rounded-lg">
                <Calendar className="w-4 h-4 text-gray-400" />
                <span className="text-white">{user?.age ? `${user.age} years` : "Not provided"}</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Interests Section */}
        {user?.domain_preferences && user.domain_preferences.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm mb-6"
          >
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
              <Tag className="w-5 h-5" />
              Interests & Preferences
            </h2>
            <div className="flex flex-wrap gap-2">
              {user.domain_preferences.map((domain, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 rounded-full text-sm font-medium"
                >
                  {domain}
                </span>
              ))}
            </div>
          </motion.div>
        )}

        {/* Account Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm"
        >
          <h2 className="text-xl font-bold text-white mb-4">Account Actions</h2>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => navigate("/subscription")}
              className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg text-sm font-semibold hover:from-cyan-600 hover:to-blue-600 transition-all"
            >
              Manage Subscription
            </button>
            <button
              onClick={() => navigate("/")}
              className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-sm font-medium transition-colors"
            >
              Back to Home
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Profile;

