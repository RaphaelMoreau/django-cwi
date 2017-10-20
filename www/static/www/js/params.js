function toggle_hidden(id) {
  elt=document.getElementById(id);
  if (elt) {
    if (elt.classList.contains('hidden_param')) {
      elt.classList.remove('hidden_param');
    } else {
      elt.classList.add('hidden_param');
    }
  }
}

function click_define(id) {
  toggle_hidden(id);
  toggle_hidden(id+'_reset');
  toggle_hidden(id+'_remove');
  toggle_hidden(id+'_define');
  document.getElementById(id+'_act').value='add';
  return false;
}

function click_remove(id) {
  toggle_hidden(id);
  toggle_hidden(id+'_reset');
  toggle_hidden(id+'_remove');
  toggle_hidden(id+'_define');
  document.getElementById(id+'_act').value='del';
  return false;
}

function click_reset(id) {
  fld=document.getElementById(id);
  switch (fld.type) {
    case 'checkbox':
      v=(fld.getAttribute('default')=='True');
      if (v != fld.checked) {
        fld.click();
      }
      break;
    default:
      fld.value=fld.getAttribute('default');
      break;
  }
  return false;
}

function changed(self) {
  f=document.getElementById(self.id+'_reset');
  if (!f) {
    console.log("No reset");
    return;
  }
  switch (self.type) {
    case 'checkbox':
      v=(self.checked)?'True':'False';
      break;
    default:
      v=self.value;
      break;
  }
  c=self.getAttribute('default');
  console.log("v="+v+" c="+c);
  f.disabled = (v==c);
}

function ShowOrHide(self,id) {
  f=document.getElementById(id);
  a=document.getElementById(id+'_act');
  if (self.textContent=='Define') {
    f.classList.remove('hidden_param');
    a.value='add';
    self.textContent='Remove';
  } else {
    f.classList.add('hidden_param');
    a.value='del';
    self.textContent='Define';
  }
  return false;
}
