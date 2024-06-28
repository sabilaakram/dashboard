import React from 'react'

function Cards({text, subtext, icon}) {
  return (
    <div>
      <div>
            <div className='md:w-48 bg-slate-100 shadow-sm shadow-slate-400 md:h-16 gap-4 md:flex justify-center items-center'>
              <div className='rounded-full bg-lime-300 md:p-2 md:h-10 md:w-10 flex items-center justify-center'>
                {icon}
              </div>
              <div>
                <p className='font-bold'>
                  {text}
                </p>
                <p className='text-gray-600  text-sm'>
                    {subtext}                </p>
              </div>
            </div>
          </div>
    </div>
  )
}

export default Cards
