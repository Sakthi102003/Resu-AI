import React from "react";
import { motion } from "framer-motion";

const Marquee = ({ items, direction = "left", speed = 20, className = "" }) => {
    return (
        <div className={`flex overflow-hidden whitespace-nowrap py-3 ${className}`}>
            <motion.div
                className="flex min-w-full items-center gap-8 px-4"
                animate={{
                    x: direction === "left" ? ["0%", "-100%"] : ["-100%", "0%"],
                }}
                transition={{
                    duration: speed,
                    repeat: Infinity,
                    ease: "linear",
                }}
            >
                {items.map((item, index) => (
                    <span key={index} className="text-4xl font-bold uppercase tracking-widest opacity-80">
                        {item} •
                    </span>
                ))}
                {items.map((item, index) => (
                    <span key={`dup-${index}`} className="text-4xl font-bold uppercase tracking-widest opacity-80">
                        {item} •
                    </span>
                ))}
                {items.map((item, index) => (
                    <span key={`dup2-${index}`} className="text-4xl font-bold uppercase tracking-widest opacity-80">
                        {item} •
                    </span>
                ))}
            </motion.div>
            <motion.div
                className="flex min-w-full items-center gap-8 px-4"
                animate={{
                    x: direction === "left" ? ["0%", "-100%"] : ["-100%", "0%"],
                }}
                transition={{
                    duration: speed,
                    repeat: Infinity,
                    ease: "linear",
                }}
                aria-hidden="true"
            >
                {items.map((item, index) => (
                    <span key={index} className="text-4xl font-bold uppercase tracking-widest opacity-80">
                        {item} •
                    </span>
                ))}
                {items.map((item, index) => (
                    <span key={`dup-${index}`} className="text-4xl font-bold uppercase tracking-widest opacity-80">
                        {item} •
                    </span>
                ))}
                {items.map((item, index) => (
                    <span key={`dup2-${index}`} className="text-4xl font-bold uppercase tracking-widest opacity-80">
                        {item} •
                    </span>
                ))}
            </motion.div>
        </div>
    );
};

export default Marquee;
