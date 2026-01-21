import { Link, useLocation } from "react-router-dom"
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"

export function Navbar() {
  const location = useLocation()

  return (
    <div className="flex w-screen bg-sidebar border-accent-foreground border-b justify-center">
      <div className="flex h-16 items-center pr-8 max-w-6xl w-full">
        <NavigationMenu>
          <NavigationMenuList>
            <p className="mr-8 font-bold">
                Edgrant's Dataroom
            </p>

            <NavigationMenuItem>
              <Link to="/">
                <NavigationMenuLink 
                  className={navigationMenuTriggerStyle() + " shadow"}
                  active={location.pathname === "/"}
                >
                  AI Chat
                </NavigationMenuLink>
              </Link>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <Link to="/challenge">
                <NavigationMenuLink 
                  className={navigationMenuTriggerStyle() + " shadow"}
                  active={location.pathname === "/challenge"}
                >
                  Challenge Description
                </NavigationMenuLink>
              </Link>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
    </div>
  )
}
