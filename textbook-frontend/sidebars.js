/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Physical AI Concepts',
      items: ['concepts/intro', 'concepts/fundamentals', 'concepts/applications'],
    },
    {
      type: 'category',
      label: 'Interactive Tutorials',
      items: ['tutorials/intro', 'tutorials/hands-on', 'tutorials/advanced'],
    },
    {
      type: 'category',
      label: 'Research Papers',
      items: ['papers/intro', 'papers/methods', 'papers/results'],
    },
  ],
};

module.exports = sidebars;