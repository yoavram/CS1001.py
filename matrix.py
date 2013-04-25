class Matrix:
    
    def __init__(self, n_rows, m_cols, default_value=0):
        '''n_rows is number of rows, ...'''
        assert isinstance(n_rows, int) and isinstance(m_cols,int) 
        assert n_rows > 0 and m_cols > 0
        self.rows = [[default_value for j in range(m_cols) ] for i in range(n_rows)]
            
    def dim(self):
        '''return tuple -> num of rows, num of cols'''
        return len(self.rows), len(self.rows[0])
    
    def __repr__(self):
        return '<Matrix %d,%d>: \n' % self.dim() + str(self.rows[0][:min(5,self.dim()[1])])
    
    def __eq__(self, other):
        assert isinstance(other, Matrix)
        if self.dim() != other.dim(): 
            return False
        n,m = self.dim()
        for i in range(n):
            for j in range(m):
                if self[i,j] != other[i,j]:
                    return False
        return True
    
    def ___getitem__(self,index):
        return self.rows[index]
        
    def __getitem__(self, ij): 
        '''ij is a tuple (i,j). Allows m[i,j] instead m[i][j]'''
        i,j = ij
        if isinstance(i, int) and isinstance(j, int):
            return self.rows[i][j]
        elif isinstance(i, slice) and isinstance(j, slice):
            M = Matrix(1,1) # to be overwritten
            M.rows = [row[j] for row in self.rows[i]]
            return M
        else:
            return NotImplemented
    
    def __setitem__(self, ij, val): 
        '''ij is a tuple (i,j). Allows m[i,j] instead m[i][j]'''
        i,j = ij
        if isinstance(i,int) and isinstance(j,int):
            #assert isinstance(val, (int, float, complex))
            self.rows[i][j] = val
        elif isinstance(i,slice) and isinstance(j,slice):
            assert isinstance(val, Matrix)
            n,m = val.dim()
            s_rows = self.rows[i]
            assert len(s_rows) == n and len(s_rows[0][j]) == m
            for s_row, v_row in zip(s_rows,val.rows):
                s_row[j] = v_row
        else:
            return NotImplemented
    
    def __str__(self):
        return '\n'.join([ str(row) for row in self.rows ])
    
    def __add__(self, other):
        return self._entrywise_op(other, lambda x,y: x + y)
       
    def __sub__(self, other):
        return self._entrywise_op(other, lambda x,y: x - y)
    
    def __neg__(self):
        n,m = self.dim()
        return Matrix(n,m,0) - self        
    
    def _entrywise_op(self, other, op):
        assert isinstance(other, Matrix)
        assert self.dim() == other.dim()
        n,m = self.dim()
        M = Matrix(n,m)
        for i in range(n):
            for j in range(m):
                M[i,j] = op(self[i,j], other[i,j])
        return M
        
    
    def __mul__(self, other):
        '''multilpy by scalar or another matrix'''
        n,m = self.dim()
        if isinstance(other, (float, int)):
            return self._entrywise_op(Matrix(n,m,other), lambda x,y: x * y)
        elif isinstance(other, Matrix):
            return self._entrywise_op(other, lambda x,y: x * y)
        else:
            return NotImplemented
        
    __rmul__ = __mul__
    
    def save(self, filename):
        '''save to file'''
        with open(filename,'w') as fout:
            print(self, file=fout)
    
    @staticmethod
    def load(filename):
        '''load from file'''
        M = Matrix(1,1)
        M.rows = []
        with open(filename) as fin:
            for line in fin:
                line = line.strip()
                row = eval(line)
                M.rows.append(row)
        return M
