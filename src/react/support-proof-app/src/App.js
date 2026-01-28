import React, { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Box, List, ListItem } from '@mui/material';

function App() {
  const [annihilator, setAnnihilator] = useState(['x', 'y', 'z']);
  const [primes, setPrimes] = useState([
    ['x', 'y', 'z', 'a', 'b'],
    ['x', 'y', 'a', 'b'],
    ['x', 'y', 'z', 'c', 'd'],
    ['x', 'a', 'b', 'c']
  ]);

  const calculateV = () => {
    return primes.filter(p => 
      annihilator.every(a => p.includes(a))
    );
  };

  const vI = calculateV();

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Support Module Proof
        </Typography>
        
        <Typography variant="h6" sx={{ mt: 3 }}>
          Theorem: Supp(M) ⊆ V(Ann(M))
        </Typography>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1">Annihilator I:</Typography>
          <Typography variant="body1">{`{${annihilator.join(', ')}}`}</Typography>
        </Box>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1">Prime Ideals:</Typography>
          <List>
            {primes.map((p, i) => (
              <ListItem key={i}>
                p{i+1} = {`{${p.join(', ')}}`}
                {annihilator.every(a => p.includes(a)) ? ' ∈ V(I)' : ' ∉ V(I)'}
              </ListItem>
            ))}
          </List>
        </Box>
        
        <Box sx={{ mt: 3, p: 2, bgcolor: '#e8f5e9' }}>
          <Typography variant="h6">Result:</Typography>
          <Typography variant="body1">
            V(I) = {`{${vI.map((_, i) => `p${primes.indexOf(vI[i]) + 1}`).join(', ')}}`}
          </Typography>
          <Typography variant="body1" sx={{ mt: 1 }}>
            Since any p ∈ Supp(M) must satisfy I ⊆ p, we have:
          </Typography>
          <Typography variant="body1" sx={{ fontWeight: 'bold', color: 'green' }}>
            Supp(M) ⊆ V(I)
          </Typography>
        </Box>
        
        <Box sx={{ mt: 4, p: 2, bgcolor: '#f5f5f5' }}>
          <Typography variant="h6">Proof Sketch:</Typography>
          <Typography variant="body2">
            1. Take p ∈ Supp(M) (M_p ≠ 0)<br/>
            2. Suppose I ⊈ p → ∃a ∈ I, a ∉ p<br/>
            3. a ∉ p ⇒ a is unit in A_p<br/>
            4. But a ∈ Ann(M) ⇒ aM = 0<br/>
            5. Localize: (a/1)M_p = 0<br/>
            6. Since a/1 invertible, M_p = 0<br/>
            7. Contradiction! So I ⊆ p<br/>
            8. Therefore p ∈ V(I)
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default App;
