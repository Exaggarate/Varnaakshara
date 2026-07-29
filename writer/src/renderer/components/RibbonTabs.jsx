import React, { useState } from 'react';

const TABS = ['Home', 'Insert', 'Layout', 'Review', 'Tools'];

export default function RibbonTabs({ activeTab, onTabChange }) {
  return (
    <div className="ribbon-tabs">
      {TABS.map((tab) => (
        <button
          key={tab}
          className={`ribbon-tab ${activeTab === tab ? 'active' : ''}`}
          onClick={() => onTabChange(tab)}
        >
          {tab}
        </button>
      ))}
    </div>
  );
}
