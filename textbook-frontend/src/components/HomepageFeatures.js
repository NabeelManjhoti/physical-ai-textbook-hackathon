import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Interactive Learning',
    description: (
      <>
        Engage with interactive examples and simulations that bring Physical AI concepts to life.
      </>
    ),
  },
  {
    title: 'Research-Driven',
    description: (
      <>
        Learn from cutting-edge research in robotics, computer vision, and embodied intelligence.
      </>
    ),
  },
  {
    title: 'Hands-On Practice',
    description: (
      <>
        Apply concepts through practical exercises and projects with real-world applications.
      </>
    ),
  },
];

function Feature({ Svg, title, description }) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}