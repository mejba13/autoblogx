import Link from 'next/link';

export default function LandingPage() {
  return (
    <main className="flex flex-col min-h-screen bg-gray-50">
      {/* Navbar */}
      <header className="flex items-center justify-between p-6 bg-white shadow-sm">
      <h1 className="text-xl font-bold text-gray-800">AutoBlogX</h1>
      <div className="space-x-4">
        {/* Django /auth/register/ route */}
        <a href="http://127.0.0.1:8000/auth/register/" target="_blank" rel="noopener noreferrer">
          <button className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700">
            Register
          </button>
        </a>

        {/* Django /auth/login/ route */}
        <a href="http://127.0.0.1:8000/auth/login/" target="_blank" rel="noopener noreferrer">
          <button className="px-4 py-2 rounded border border-indigo-600 text-indigo-600 hover:bg-indigo-50">
            Login
          </button>
        </a>
      </div>
    </header>

      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center text-center py-24 px-4">
        <h2 className="text-4xl font-extrabold text-gray-900 mb-4">🚀 Welcome to AutoBlogX</h2>
        <p className="max-w-2xl text-lg text-gray-600 mb-6">
          <span className="text-indigo-600 font-medium">AutoBlogX</span> is your all-in-one AI-powered blog automation solution. <br />
          Create, optimize, and publish content that drives traffic — effortlessly.
        </p>
        <Link href="/register">
          <button className="px-6 py-3 rounded bg-indigo-600 text-white font-medium hover:bg-indigo-700">
            Get Started
          </button>
        </Link>
      </section>

      {/* Features */}
      <section className="bg-white py-20 px-6">
        <div className="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <Feature title="AI Content Generation" description="Generate premium blog posts powered by AI with a single click." />
          <Feature title="Media Automation" description="Automatically attach optimized images and videos to each article." />
          <Feature title="SEO Smart" description="Enhance your content for search engines without manual work." />
          <Feature title="Schedule & Publish" description="Publish instantly or schedule your posts at optimal times." />
          <Feature title="Insights & Trends" description="Stay ahead with trending topic suggestions and analytics." />
          <Feature title="Built with Love" description="Next.js, Django, TailwindCSS — modern stack, blazing speed." />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-100 py-6 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AutoBlogX. All rights reserved.
      </footer>
    </main>
  );
}

function Feature({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-all">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );
}