import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Platform icons mapping
const PLATFORM_ICONS = {
  twitter: '🐦',
  facebook: '📘',
  instagram: '📸',
  linkedin: '💼',
  tiktok: '🎵',
  youtube: '📺',
  pinterest: '📌',
  reddit: '🔶',
  discord: '🎮',
  telegram: '✈️'
};

// Calendar Component
const Calendar = ({ posts, onDateSelect }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [calendarPosts, setCalendarPosts] = useState([]);

  useEffect(() => {
    fetchCalendarPosts();
  }, [currentDate]);

  const fetchCalendarPosts = async () => {
    try {
      const startDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
      const endDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
      
      const response = await axios.get(`${API}/posts/calendar`, {
        params: {
          start_date: startDate.toISOString(),
          end_date: endDate.toISOString()
        }
      });
      setCalendarPosts(response.data);
    } catch (error) {
      console.error('Error fetching calendar posts:', error);
    }
  };

  const getDaysInMonth = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days = [];
    
    // Add empty cells for days before the first day of the month
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }
    
    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day);
    }
    
    return days;
  };

  const getPostsForDay = (day) => {
    if (!day) return [];
    
    const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    return calendarPosts.filter(post => {
      const postDate = new Date(post.scheduled_time || post.published_time);
      return postDate.getDate() === day &&
             postDate.getMonth() === dayDate.getMonth() &&
             postDate.getFullYear() === dayDate.getFullYear();
    });
  };

  const previousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={previousMonth}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          ←
        </button>
        <h2 className="text-2xl font-bold text-gray-800">
          {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
        </h2>
        <button
          onClick={nextMonth}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          →
        </button>
      </div>

      <div className="grid grid-cols-7 gap-1 mb-2">
        {dayNames.map(day => (
          <div key={day} className="p-2 text-center font-semibold text-gray-600 bg-gray-100 rounded">
            {day}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-7 gap-1">
        {getDaysInMonth().map((day, index) => {
          const dayPosts = getPostsForDay(day);
          const isToday = day && 
            new Date().getDate() === day &&
            new Date().getMonth() === currentDate.getMonth() &&
            new Date().getFullYear() === currentDate.getFullYear();

          return (
            <div
              key={index}
              className={`min-h-[100px] p-2 border border-gray-200 rounded-lg ${
                day ? 'bg-white hover:bg-gray-50 cursor-pointer' : 'bg-gray-50'
              } ${isToday ? 'ring-2 ring-blue-500 bg-blue-50' : ''}`}
              onClick={() => day && onDateSelect && onDateSelect(new Date(currentDate.getFullYear(), currentDate.getMonth(), day))}
            >
              {day && (
                <>
                  <div className={`text-sm font-medium mb-1 ${isToday ? 'text-blue-600' : 'text-gray-700'}`}>
                    {day}
                  </div>
                  <div className="space-y-1">
                    {dayPosts.slice(0, 3).map(post => (
                      <div
                        key={post.id}
                        className={`text-xs p-1 rounded truncate ${
                          post.status === 'published' ? 'bg-green-100 text-green-800' :
                          post.status === 'scheduled' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}
                        title={post.title}
                      >
                        {post.platforms.map(platform => PLATFORM_ICONS[platform]).join('')} {post.title}
                      </div>
                    ))}
                    {dayPosts.length > 3 && (
                      <div className="text-xs text-gray-500">
                        +{dayPosts.length - 3} more
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Analytics Chart Component
const AnalyticsChart = ({ data, title, color = 'blue' }) => {
  const maxValue = Math.max(...data.map(d => d.value));
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      <div className="space-y-3">
        {data.map((item, index) => (
          <div key={index} className="flex items-center justify-between">
            <span className="text-sm text-gray-600 w-20">{item.label}</span>
            <div className="flex-1 mx-3">
              <div className="bg-gray-200 rounded-full h-4 relative">
                <div
                  className={`bg-${color}-500 rounded-full h-4 transition-all duration-500`}
                  style={{ width: `${(item.value / maxValue) * 100}%` }}
                ></div>
              </div>
            </div>
            <span className="text-sm font-medium text-gray-800 w-12 text-right">
              {item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// Advanced Analytics Dashboard
const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState({});
  const [posts, setPosts] = useState([]);
  const [timeRange, setTimeRange] = useState('7d');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyticsData();
  }, [timeRange]);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const [analyticsResponse, postsResponse] = await Promise.all([
        axios.get(`${API}/analytics/dashboard`),
        axios.get(`${API}/posts`)
      ]);
      
      setAnalytics(analyticsResponse.data);
      setPosts(postsResponse.data);
      
      // Process analytics data for charts
      processAnalyticsData(analyticsResponse.data, postsResponse.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const processAnalyticsData = (analyticsData, postsData) => {
    // This would process real analytics data
    // For now, we'll use the data we have
  };

  const engagementData = [
    { label: 'Twitter', value: 45 },
    { label: 'LinkedIn', value: 32 },
    { label: 'TikTok', value: 78 },
    { label: 'Instagram', value: 56 }
  ];

  const postPerformanceData = [
    { label: 'Mon', value: 12 },
    { label: 'Tue', value: 8 },
    { label: 'Wed', value: 15 },
    { label: 'Thu', value: 22 },
    { label: 'Fri', value: 18 },
    { label: 'Sat', value: 25 },
    { label: 'Sun', value: 14 }
  ];

  const platformDistribution = posts.reduce((acc, post) => {
    post.platforms.forEach(platform => {
      acc[platform] = (acc[platform] || 0) + 1;
    });
    return acc;
  }, {});

  const platformData = Object.entries(platformDistribution).map(([platform, count]) => ({
    label: platform.charAt(0).toUpperCase() + platform.slice(1),
    value: count
  }));

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="spinner"></div>
        <span className="ml-2 text-gray-600">Loading analytics...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Time Range Selector */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Analytics Dashboard</h1>
        <div className="flex space-x-2">
          {['7d', '30d', '90d'].map(range => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                timeRange === range
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {range === '7d' ? '7 Days' : range === '30d' ? '30 Days' : '90 Days'}
            </button>
          ))}
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-md p-6 text-white">
          <h3 className="text-lg font-medium mb-2">Total Posts</h3>
          <p className="text-3xl font-bold">{analytics.total_posts || 0}</p>
          <p className="text-blue-100 text-sm">+12% from last period</p>
        </div>
        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg shadow-md p-6 text-white">
          <h3 className="text-lg font-medium mb-2">Published</h3>
          <p className="text-3xl font-bold">{analytics.published_posts || 0}</p>
          <p className="text-green-100 text-sm">+8% from last period</p>
        </div>
        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg shadow-md p-6 text-white">
          <h3 className="text-lg font-medium mb-2">Scheduled</h3>
          <p className="text-3xl font-bold">{analytics.scheduled_posts || 0}</p>
          <p className="text-purple-100 text-sm">+5% from last period</p>
        </div>
        <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg shadow-md p-6 text-white">
          <h3 className="text-lg font-medium mb-2">Total Engagement</h3>
          <p className="text-3xl font-bold">2.4K</p>
          <p className="text-orange-100 text-sm">+18% from last period</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnalyticsChart
          title="Platform Engagement Rate"
          data={engagementData}
          color="blue"
        />
        <AnalyticsChart
          title="Posts by Platform"
          data={platformData}
          color="green"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
        <AnalyticsChart
          title="Post Performance This Week"
          data={postPerformanceData}
          color="purple"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {analytics.recent_analytics?.slice(0, 5).map((analytic, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm text-gray-600">
                  Post analytics updated for {analytic.platform}
                </span>
              </div>
              <span className="text-xs text-gray-500">
                {new Date(analytic.created_at).toLocaleDateString()}
              </span>
            </div>
          )) || (
            <p className="text-gray-500 text-center py-4">No recent activity</p>
          )}
        </div>
      </div>

      {/* Top Performing Posts */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Top Performing Posts</h3>
        <div className="space-y-4">
          {posts.filter(post => post.status === 'published').slice(0, 5).map(post => (
            <div key={post.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex-1">
                <h4 className="font-medium text-gray-800">{post.title}</h4>
                <p className="text-sm text-gray-600 mt-1">{post.content.substring(0, 100)}...</p>
                <div className="flex items-center space-x-2 mt-2">
                  {post.platforms.map(platform => (
                    <span key={platform} className="text-lg">
                      {PLATFORM_ICONS[platform]}
                    </span>
                  ))}
                  <span className="text-xs text-gray-500">
                    {new Date(post.published_time).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-800">Engagement</div>
                <div className="text-lg font-bold text-blue-600">
                  {Math.floor(Math.random() * 100) + 20}%
                </div>
              </div>
            </div>
          ))}
          {posts.filter(post => post.status === 'published').length === 0 && (
            <p className="text-gray-500 text-center py-4">No published posts yet</p>
          )}
        </div>
      </div>
    </div>
  );
};

// Post Creation Component
const PostCreator = ({ onPostCreated, onCancel }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [platforms, setPlatforms] = useState([]);
  const [scheduledTime, setScheduledTime] = useState('');
  const [mediaFiles, setMediaFiles] = useState([]);

  const handlePlatformToggle = (platform) => {
    setPlatforms(prev => 
      prev.includes(platform) 
        ? prev.filter(p => p !== platform)
        : [...prev, platform]
    );
  };

  const handleMediaUpload = (event) => {
    const files = Array.from(event.target.files);
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        setMediaFiles(prev => [...prev, e.target.result]);
      };
      reader.readAsDataURL(file);
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const postData = {
        title,
        content,
        platforms,
        media_files: mediaFiles,
        scheduled_time: scheduledTime ? new Date(scheduledTime).toISOString() : null
      };

      await axios.post(`${API}/posts`, postData);
      onPostCreated();
      setTitle('');
      setContent('');
      setPlatforms([]);
      setScheduledTime('');
      setMediaFiles([]);
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">Create New Post</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Content
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows="4"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Platforms
          </label>
          <div className="grid grid-cols-5 gap-2">
            {Object.entries(PLATFORM_ICONS).map(([platform, icon]) => (
              <button
                key={platform}
                type="button"
                onClick={() => handlePlatformToggle(platform)}
                className={`p-3 rounded-lg border-2 transition-colors ${
                  platforms.includes(platform)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <div className="text-2xl mb-1">{icon}</div>
                <div className="text-xs capitalize">{platform}</div>
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Schedule Time (Optional)
          </label>
          <input
            type="datetime-local"
            value={scheduledTime}
            onChange={(e) => setScheduledTime(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Media Files
          </label>
          <input
            type="file"
            multiple
            accept="image/*,video/*"
            onChange={handleMediaUpload}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {mediaFiles.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-2">
              {mediaFiles.map((file, index) => (
                <div key={index} className="relative">
                  <img
                    src={file}
                    alt={`Preview ${index + 1}`}
                    className="w-20 h-20 object-cover rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => setMediaFiles(prev => prev.filter((_, i) => i !== index))}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flex space-x-3">
          <button
            type="submit"
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
          >
            Create Post
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

// Post Card Component
const PostCard = ({ post, onEdit, onDelete, onPublish }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800';
      case 'scheduled': return 'bg-blue-100 text-blue-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-800">{post.title}</h3>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(post.status)}`}>
          {post.status}
        </span>
      </div>
      
      <p className="text-gray-600 mb-4">{post.content}</p>
      
      {post.media_files && post.media_files.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {post.media_files.map((file, index) => (
              <img
                key={index}
                src={file}
                alt={`Media ${index + 1}`}
                className="w-16 h-16 object-cover rounded-lg"
              />
            ))}
          </div>
        </div>
      )}
      
      <div className="flex justify-between items-center mb-4">
        <div className="flex space-x-2">
          {post.platforms.map(platform => (
            <span key={platform} className="text-lg">
              {PLATFORM_ICONS[platform]}
            </span>
          ))}
        </div>
        
        {post.scheduled_time && (
          <span className="text-sm text-gray-500">
            Scheduled: {new Date(post.scheduled_time).toLocaleString()}
          </span>
        )}
      </div>
      
      <div className="flex space-x-2">
        <button
          onClick={() => onEdit(post)}
          className="px-3 py-1 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
        >
          Edit
        </button>
        {post.status !== 'published' && (
          <button
            onClick={() => onPublish(post.id)}
            className="px-3 py-1 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
          >
            Publish
          </button>
        )}
        <button
          onClick={() => onDelete(post.id)}
          className="px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [posts, setPosts] = useState([]);
  const [showPostCreator, setShowPostCreator] = useState(false);
  const [analytics, setAnalytics] = useState({});

  useEffect(() => {
    fetchPosts();
    fetchAnalytics();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get(`${API}/posts`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API}/analytics/dashboard`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const handlePostCreated = () => {
    setShowPostCreator(false);
    fetchPosts();
    fetchAnalytics();
  };

  const handlePublish = async (postId) => {
    try {
      await axios.post(`${API}/posts/${postId}/publish`);
      fetchPosts();
      fetchAnalytics();
    } catch (error) {
      console.error('Error publishing post:', error);
    }
  };

  const handleDelete = async (postId) => {
    try {
      await axios.delete(`${API}/posts/${postId}`);
      fetchPosts();
      fetchAnalytics();
    } catch (error) {
      console.error('Error deleting post:', error);
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      {/* Hero Section */}
      <div 
        className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white"
        style={{
          backgroundImage: 'linear-gradient(rgba(59, 130, 246, 0.8), rgba(147, 51, 234, 0.8)), url("https://images.unsplash.com/photo-1511707171634-5f897ff02aa9")',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <h1 className="text-4xl font-bold mb-4">Social Media Management Platform</h1>
        <p className="text-xl mb-6">Plan, publish, and analyze your content across all social channels</p>
        <button
          onClick={() => setShowPostCreator(true)}
          className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
        >
          Create New Post
        </button>
      </div>

      {/* Analytics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Total Posts</h3>
          <p className="text-3xl font-bold text-blue-600">{analytics.total_posts || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Published</h3>
          <p className="text-3xl font-bold text-green-600">{analytics.published_posts || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Scheduled</h3>
          <p className="text-3xl font-bold text-blue-600">{analytics.scheduled_posts || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Drafts</h3>
          <p className="text-3xl font-bold text-gray-600">{analytics.draft_posts || 0}</p>
        </div>
      </div>

      {/* Recent Posts */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4">Recent Posts</h2>
        {posts.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No posts yet. Create your first post to get started!</p>
        ) : (
          <div className="space-y-4">
            {posts.slice(0, 3).map(post => (
              <PostCard
                key={post.id}
                post={post}
                onEdit={() => {}}
                onDelete={handleDelete}
                onPublish={handlePublish}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderPosts = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">All Posts</h1>
        <button
          onClick={() => setShowPostCreator(true)}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Create New Post
        </button>
      </div>

      {posts.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg mb-4">No posts yet. Create your first post to get started!</p>
          <button
            onClick={() => setShowPostCreator(true)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Create Your First Post
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map(post => (
            <PostCard
              key={post.id}
              post={post}
              onEdit={() => {}}
              onDelete={handleDelete}
              onPublish={handlePublish}
            />
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-800">SocialHub</h1>
            </div>
            <div className="flex items-center space-x-8">
              <button
                onClick={() => setCurrentView('dashboard')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'dashboard' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setCurrentView('posts')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'posts' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Posts
              </button>
              <button
                onClick={() => setCurrentView('calendar')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'calendar' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Calendar
              </button>
              <button
                onClick={() => setCurrentView('analytics')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'analytics' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Analytics
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {showPostCreator && (
          <PostCreator
            onPostCreated={handlePostCreated}
            onCancel={() => setShowPostCreator(false)}
          />
        )}

        {currentView === 'dashboard' && renderDashboard()}
        {currentView === 'posts' && renderPosts()}
        {currentView === 'calendar' && (
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Calendar View</h2>
            <p className="text-gray-600">Calendar view coming soon...</p>
          </div>
        )}
        {currentView === 'analytics' && (
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Analytics Dashboard</h2>
            <p className="text-gray-600">Advanced analytics coming soon...</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;