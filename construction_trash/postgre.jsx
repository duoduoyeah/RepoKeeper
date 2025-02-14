import React from 'react';
import { ArrowRight, Database, Server, Monitor, Globe, Terminal } from 'lucide-react';

const PostgreSQLArchitecture = () => {
    return (
        <div className="p-8 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-8 text-center text-gray-800">
                PostgreSQL Client/Server Architecture
            </h2>
            
            <div className="flex flex-col md:flex-row items-center justify-between gap-8 bg-gray-50 p-6 rounded-lg shadow-lg">
                {/* Client Side */}
                <div className="space-y-4">
                    <div className="text-center font-semibold mb-4 text-gray-700">
                        Client Applications
                    </div>
                    <div className="space-y-4">
                        <div className="flex items-center gap-2 bg-blue-100 p-3 rounded-lg">
                            <Terminal className="w-5 h-5 text-blue-600" />
                            <span className="text-sm">Command-line Tool</span>
                        </div>
                        <div className="flex items-center gap-2 bg-blue-100 p-3 rounded-lg">
                            <Monitor className="w-5 h-5 text-blue-600" />
                            <span className="text-sm">GUI Application</span>
                        </div>
                        <div className="flex items-center gap-2 bg-blue-100 p-3 rounded-lg">
                            <Globe className="w-5 h-5 text-blue-600" />
                            <span className="text-sm">Web Server</span>
                        </div>
                    </div>
                </div>

                {/* Arrow */}
                <div className="flex flex-col items-center gap-2">
                    <ArrowRight className="w-8 h-8 text-gray-600 rotate-90 md:rotate-0" />
                    <div className="text-sm text-gray-600 text-center">
                        Database
                        <br />
                        Connections
                    </div>
                </div>

                {/* Server Side */}
                <div className="space-y-4">
                    <div className="text-center font-semibold mb-4 text-gray-700">
                        Server (postgres)
                    </div>
                    <div className="flex flex-col gap-4">
                        <div className="flex items-center gap-2 bg-green-100 p-3 rounded-lg">
                            <Server className="w-5 h-5 text-green-600" />
                            <span className="text-sm">Process Manager</span>
                        </div>
                        <div className="flex items-center gap-2 bg-green-100 p-3 rounded-lg">
                            <Database className="w-5 h-5 text-green-600" />
                            <span className="text-sm">Database Files</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-6 text-sm text-gray-600">
                <ul className="list-disc pl-5 space-y-2">
                    <li>Server process (postgres) manages database files and connections</li>
                    <li>Multiple client applications can connect simultaneously</li>
                    <li>Client applications can be custom-built or PostgreSQL-provided</li>
                </ul>
            </div>
        </div>
    );
};

export default PostgreSQLArchitecture;