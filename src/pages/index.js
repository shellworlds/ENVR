import React from 'react';
import Head from 'next/head';
import ModuleSplitterReact from '../ModuleSplitterReact';

const HomePage = () => {
    return (
        <>
            <Head>
                <title>ENVR Module Splitter | Next.js Implementation</title>
                <meta name="description" content="Interactive proof of the Module Splitting Theorem" />
            </Head>
            <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
                <h1>ENVR Module Splitter - Next.js Implementation</h1>
                <p>Module Splitting Theorem Visualization</p>
                <ModuleSplitterReact />
                <div style={{ marginTop: '40px', padding: '20px', background: '#f5f5f5', borderRadius: '10px' }}>
                    <h3>Theorem Summary</h3>
                    <p>M = L ⊕ N with α=i<sub>L</sub>, β=π<sub>N</sub>, σ=i<sub>N</sub>, ρ=π<sub>L</sub></p>
                    <p>iff βα=0, βσ=1, ρσ=0, ρα=1, αρ+σβ=1</p>
                </div>
            </div>
        </>
    );
};

export default HomePage;
