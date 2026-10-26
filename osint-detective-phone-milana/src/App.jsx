import { useState } from 'react';
import LockScreen from './screens/LockScreen';
import HomeScreen from './screens/HomeScreen';
import FileManager from './screens/FileManager';
import MilanaPhone from './screens/MilanaPhone';
import BrowserError from './screens/BrowserError';
import GlobalShade from './components/GlobalShade';
import BrokenScreen from './components/BrokenScreen';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('lock');
  const [milanaInitial, setMilanaInitial] = useState('threads');
  const [previousScreen, setPreviousScreen] = useState('home');

  const openMilana = (initial, from) => {
    setMilanaInitial(initial);
    setPreviousScreen(from);
    setCurrentScreen('milana-phone');
  };

  const handleOpenApp = (app) => {
    if (app === 'messages') openMilana('threads', 'home');
    else if (app === 'phone') openMilana('phone', 'home');
    else if (app === 'gallery') openMilana('gallery', 'home');
    else if (app === 'settings') openMilana('settings', 'home');
    else if (app === 'notes') openMilana('notes', 'home');
    else if (app === 'maps') openMilana('maps', 'home');
    else if (app === 'camera') openMilana('camera', 'home');
    else if (app === 'files') setCurrentScreen('files');
    else if (app === 'browser') setCurrentScreen('browser-error');
  };

  const handleBack = () => {
    if (currentScreen === 'milana-phone') setCurrentScreen(previousScreen);
    else setCurrentScreen('home');
  };

  const showGlobalShade = currentScreen !== 'lock';

  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <div className="w-96 h-screen max-h-[800px] bg-zinc-900 rounded-[48px] p-2.5 shadow-2xl overflow-hidden border-8 border-zinc-950">
        <div className="w-full h-full bg-zinc-950 rounded-[40px] overflow-hidden flex flex-col relative">

          <div className="absolute top-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-black rounded-full z-50"></div>

          {showGlobalShade && (
            <GlobalShade onOpenThread={() => openMilana('threads', 'home')} />
          )}

          <div className="flex-1 overflow-hidden">
            {currentScreen === 'lock' && <LockScreen onUnlock={() => setCurrentScreen('home')} />}
            {currentScreen === 'home' && <HomeScreen onOpenApp={handleOpenApp} />}
            {currentScreen === 'files' && <FileManager onBack={handleBack} />}
            {currentScreen === 'browser-error' && <BrowserError onBack={handleBack} />}
            {currentScreen === 'milana-phone' && (
              <MilanaPhone onBack={handleBack} initialScreen={milanaInitial} />
            )}
          </div>

          <BrokenScreen />
        </div>
      </div>
    </div>
  );
}