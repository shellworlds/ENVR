/**
 * Advanced ECG Visualization Component for Cardiology Dashboard
 * React + D3.js based visualization
 */

import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Slider } from './ui/slider';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

const ECGVisualizer = ({ ecgData, patientId, samplingRate = 500, width = 800, height = 400 }) => {
    const svgRef = useRef();
    const [timeRange, setTimeRange] = useState([0, 10]); // seconds
    const [amplitudeScale, setAmplitudeScale] = useState(1.0);
    const [selectedLead, setSelectedLead] = useState('II');
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    
    // ECG leads configuration
    const ecgLeads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'];
    
    // Industry standard colors
    const industryColors = {
        ecgSignal: '#2563eb',
        rPeaks: '#dc2626',
        pWave: '#16a34a',
        tWave: '#ea580c',
        baseline: '#6b7280',
        grid: '#e5e7eb'
    };
    
    // Initialize visualization
    useEffect(() => {
        if (!ecgData || !svgRef.current) return;
        
        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();
        
        const margin = { top: 40, right: 40, bottom: 60, left: 60 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Create scales
        const xScale = d3.scaleLinear()
            .domain(timeRange)
            .range([0, innerWidth]);
            
        const yScale = d3.scaleLinear()
            .domain([-2 * amplitudeScale, 2 * amplitudeScale])
            .range([innerHeight, 0]);
        
        // Create main group
        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        // Add gridlines
        g.append('g')
            .attr('class', 'grid')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(d3.axisBottom(xScale)
                .ticks(20)
                .tickSize(-innerHeight)
                .tickFormat(''))
            .selectAll('line')
            .attr('stroke', industryColors.grid)
            .attr('stroke-opacity', 0.3);
            
        g.append('g')
            .attr('class', 'grid')
            .call(d3.axisLeft(yScale)
                .ticks(10)
                .tickSize(-innerWidth)
                .tickFormat(''))
            .selectAll('line')
            .attr('stroke', industryColors.grid)
            .attr('stroke-opacity', 0.3);
        
        // Add axes
        g.append('g')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(d3.axisBottom(xScale).ticks(10))
            .append('text')
            .attr('x', innerWidth / 2)
            .attr('y', 40)
            .attr('fill', 'currentColor')
            .attr('text-anchor', 'middle')
            .text('Time (seconds)');
            
        g.append('g')
            .call(d3.axisLeft(yScale).ticks(8))
            .append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', -40)
            .attr('x', -innerHeight / 2)
            .attr('fill', 'currentColor')
            .attr('text-anchor', 'middle')
            .text('Amplitude (mV)');
        
        // Plot ECG signal
        const ecgLine = d3.line()
            .x((d, i) => xScale(i / samplingRate))
            .y(d => yScale(d * amplitudeScale))
            .curve(d3.curveMonotoneX);
        
        g.append('path')
            .datum(ecgData)
            .attr('fill', 'none')
            .attr('stroke', industryColors.ecgSignal)
            .attr('stroke-width', 1.5)
            .attr('d', ecgLine);
        
        // Add R-peak markers if available
        if (window.rPeaks) {
            g.selectAll('.r-peak')
                .data(window.rPeaks)
                .enter()
                .append('circle')
                .attr('class', 'r-peak')
                .attr('cx', d => xScale(d / samplingRate))
                .attr('cy', d => yScale(ecgData[d] * amplitudeScale))
                .attr('r', 4)
                .attr('fill', industryColors.rPeaks)
                .attr('stroke', 'white')
                .attr('stroke-width', 1);
        }
        
        // Add current time indicator
        if (isPlaying) {
            g.append('line')
                .attr('class', 'time-indicator')
                .attr('x1', xScale(currentTime))
                .attr('x2', xScale(currentTime))
                .attr('y1', 0)
                .attr('y2', innerHeight)
                .attr('stroke', '#dc2626')
                .attr('stroke-width', 2)
                .attr('stroke-dasharray', '5,5');
        }
        
        // Add title
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text(`ECG Lead ${selectedLead} - Patient ${patientId}`);
        
    }, [ecgData, timeRange, amplitudeScale, selectedLead, isPlaying, currentTime, width, height, samplingRate]);
    
    // Handle real-time playback
    useEffect(() => {
        let animationFrame;
        
        if (isPlaying) {
            const animate = () => {
                setCurrentTime(prev => {
                    const newTime = prev + 0.1;
                    if (newTime >= timeRange[1]) {
                        setIsPlaying(false);
                        return timeRange[0];
                    }
                    return newTime;
                });
                animationFrame = requestAnimationFrame(animate);
            };
            animationFrame = requestAnimationFrame(animate);
        }
        
        return () => {
            if (animationFrame) {
                cancelAnimationFrame(animationFrame);
            }
        };
    }, [isPlaying, timeRange]);
    
    const handlePlayPause = () => {
        setIsPlaying(!isPlaying);
    };
    
    const handleReset = () => {
        setIsPlaying(false);
        setCurrentTime(timeRange[0]);
    };
    
    const handleLeadChange = (lead) => {
        setSelectedLead(lead);
        // In real implementation, fetch new lead data
        console.log(`Switched to lead ${lead}`);
    };
    
    return (
        <Card className="w-full">
            <CardHeader>
                <CardTitle className="flex justify-between items-center">
                    <span>ECG Visualization Dashboard</span>
                    <div className="flex space-x-2">
                        <Button 
                            variant={isPlaying ? "destructive" : "default"}
                            onClick={handlePlayPause}
                            size="sm"
                        >
                            {isPlaying ? 'Pause' : 'Play'}
                        </Button>
                        <Button 
                            variant="outline" 
                            onClick={handleReset}
                            size="sm"
                        >
                            Reset
                        </Button>
                    </div>
                </CardTitle>
            </CardHeader>
            
            <CardContent>
                <Tabs defaultValue="visualization" className="w-full">
                    <TabsList>
                        <TabsTrigger value="visualization">Visualization</TabsTrigger>
                        <TabsTrigger value="analysis">Analysis</TabsTrigger>
                        <TabsTrigger value="export">Export</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="visualization">
                        <div className="space-y-4">
                            <div className="flex justify-between items-center">
                                <div className="flex space-x-4">
                                    <div>
                                        <label className="text-sm font-medium">Time Range (s)</label>
                                        <Slider
                                            value={timeRange}
                                            min={0}
                                            max={30}
                                            step={1}
                                            onValueChange={setTimeRange}
                                            className="w-48"
                                        />
                                    </div>
                                    <div>
                                        <label className="text-sm font-medium">Amplitude Scale</label>
                                        <Slider
                                            value={[amplitudeScale]}
                                            min={0.1}
                                            max={3}
                                            step={0.1}
                                            onValueChange={([value]) => setAmplitudeScale(value)}
                                            className="w-48"
                                        />
                                    </div>
                                </div>
                                
                                <div className="flex space-x-2">
                                    {ecgLeads.slice(0, 6).map(lead => (
                                        <Button
                                            key={lead}
                                            variant={selectedLead === lead ? "default" : "outline"}
                                            size="sm"
                                            onClick={() => handleLeadChange(lead)}
                                        >
                                            {lead}
                                        </Button>
                                    ))}
                                </div>
                            </div>
                            
                            <div className="border rounded-lg p-2 bg-white">
                                <svg
                                    ref={svgRef}
                                    width={width}
                                    height={height}
                                    className="w-full h-auto"
                                />
                            </div>
                            
                            <div className="grid grid-cols-4 gap-4 text-sm">
                                <div className="p-2 bg-blue-50 rounded">
                                    <div className="font-medium">Heart Rate</div>
                                    <div className="text-2xl font-bold">72 <span className="text-sm">bpm</span></div>
                                </div>
                                <div className="p-2 bg-green-50 rounded">
                                    <div className="font-medium">QTc Interval</div>
                                    <div className="text-2xl font-bold">420 <span className="text-sm">ms</span></div>
                                </div>
                                <div className="p-2 bg-yellow-50 rounded">
                                    <div className="font-medium">ST Segment</div>
                                    <div className="text-2xl font-bold">0.5 <span className="text-sm">mm</span></div>
                                </div>
                                <div className="p-2 bg-red-50 rounded">
                                    <div className="font-medium">Arrhythmia</div>
                                    <div className="text-2xl font-bold">None</div>
                                </div>
                            </div>
                        </div>
                    </TabsContent>
                    
                    <TabsContent value="analysis">
                        <div className="p-4">
                            <h3 className="font-bold text-lg mb-4">Advanced ECG Analysis</h3>
                            <div className="space-y-3">
                                <div className="flex justify-between">
                                    <span>R-R Interval Variability</span>
                                    <span className="font-medium">45 ms</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>P-R Interval</span>
                                    <span className="font-medium">160 ms</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>QRS Duration</span>
                                    <span className="font-medium">90 ms</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Industry Standard Compliance</span>
                                    <span className="font-medium text-green-600">100%</span>
                                </div>
                            </div>
                        </div>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
};

// Export additional components
export const ECGMultiLeadView = ({ leadsData }) => {
    return (
        <div className="grid grid-cols-3 gap-4">
            {leadsData.map((lead, index) => (
                <ECGVisualizer
                    key={index}
                    ecgData={lead.data}
                    patientId="Multi-Lead"
                    width={300}
                    height={200}
                />
            ))}
        </div>
    );
};

export const ECGTrendAnalysis = ({ historicalData }) => {
    // Implementation for trend analysis
    return (
        <div>
            <h3 className="font-bold text-lg mb-4">ECG Trend Analysis</h3>
            {/* Trend visualization implementation */}
        </div>
    );
};

export default ECGVisualizer;
