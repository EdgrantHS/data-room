import { type PropsWithChildren } from "react"

interface ShimmerProps extends PropsWithChildren {
  duration?: number
}

export const Shimmer = ({ children }: ShimmerProps) => {
  return <span className="animate-pulse">{children}</span>
}
